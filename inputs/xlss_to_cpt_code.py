import definitions
import pandas as pdb
from flask import Markup
from typing import NamedTuple, Dict

SPREAD_SHEET = 'HCE_MI_EnI_UHCUSS_FISI_MLAP_Recommendation_WRank_20190925_v2.xlsx'
SHEET_NAME_MLAP = 'MLAP - Immediate Opp'
SHEET_NAME_PRIMCPT = 'PrimCPT-Ranking'
ROOT_DIR = definitions.get_project_root()
COL_PROC_CD = 'Proc_CD'
COL_RANK = 'Rank'


class CptEntry(NamedTuple):
    cpt_code: str
    cpt_desc: str
    category: str
    cpt_min_confidence_level: float
    start_date: str
    end_date: str
    enabled: bool
    cpt_cost: int


class CptRanking(NamedTuple):
    cpt_code: str
    cpt_desc: str
    service_type: str
    service_sub_type: str
    business: str
    ranking: int


class CptLookup(NamedTuple):
    cpt_code: str
    cpt_desc: str
    service_type: str
    service_sub_type: str
    business: str
    ranking: int
    category: str
    cpt_min_confidence_level: float
    start_date: str
    end_date: str
    enabled: bool
    cpt_cost: int


def _load_cpt_codes() -> Dict[str, CptLookup]:
    cpt_code_list = {}
    for key, value in CPT_RANKING_DICT.items():
        value2 = MLAP_DICT.get(key)
        # print(key, value, value2)
        value2: CptEntry
        if value2 is None:
            cpt_code_item = CptLookup(cpt_code=value.cpt_code,
                                      cpt_desc=value.cpt_desc,
                                      service_type=value.service_type,
                                      service_sub_type=value.service_sub_type,
                                      business=value.business,
                                      ranking=value.ranking,
                                      category='',
                                      cpt_min_confidence_level=0.0,
                                      start_date='',
                                      end_date='',
                                      enabled=False,
                                      cpt_cost=0)
        else:
            cpt_code_item = CptLookup(cpt_code=value.cpt_code,
                                      cpt_desc=value.cpt_desc,
                                      service_type=value.service_type,
                                      service_sub_type=value.service_sub_type,
                                      business=value.business,
                                      ranking=value.ranking,
                                      cpt_min_confidence_level=value2.cpt_min_confidence_level,
                                      category=value2.category,
                                      start_date=value2.start_date,
                                      end_date=value2.end_date,
                                      enabled=value2.enabled,
                                      cpt_cost=value2.cpt_cost)

        # print(cpt_code_item)
        cpt_code_list[key] = cpt_code_item

    return cpt_code_list


def _load_mlap_dict() -> Dict[str, CptEntry]:
    """
    This has MLAP filtered for 'Unattended/Home Sleep Studies'
    :return:
    """
    # print('Initializing MLAP_DICT')
    mlap_file = f'{ROOT_DIR}/inputs/{SPREAD_SHEET}'
    df_mlap = pdb.read_excel(mlap_file, dtype={'PrimCPT': str}, sheet_name=SHEET_NAME_MLAP, header=5)
    # print('column names', df_mlap.head())
    df_mlap = df_mlap.dropna(subset=['MLAP Category', 'PrimCPT', 'CPT_Desc', 'Case-lvl Min MLAP'])
    df_mlap = df_mlap.sort_values(by=['MLAP Category', 'PrimCPT'])

    # restrict values to this sub group for now
    df_mlap = df_mlap[df_mlap['MLAP Category'] == 'Unattended/Home Sleep Studies']

    cpt_entries = {}
    for index, row in df_mlap.iterrows():
        cpt_code = row.get('PrimCPT')
        if not cpt_code:
            continue

        # skip records that have a higher cpt_min_confidence_level entry
        cpt_min_value = float(row.get('Case-lvl Min MLAP'))
        temp_entry = cpt_entries.get(cpt_code)
        if temp_entry and temp_entry.cpt_min_confidence_level <= cpt_min_value:
            continue

        category = row.get('MLAP Category')
        cpt_code = f'{cpt_code}'
        cpt_desc = row.get('CPT_Desc')
        cpt_cost = int(row.get('Evt Pd Unit Cost'))
        cpt_entry = CptEntry(
            category=category,
            cpt_code=cpt_code,
            cpt_desc=f'{cpt_desc}',
            cpt_cost=cpt_cost,
            cpt_min_confidence_level=cpt_min_value,
            start_date='',
            end_date='',
            enabled=True
        )
        cpt_entries[cpt_code] = cpt_entry

    return cpt_entries


def _init_prim_cpt() -> pdb.DataFrame:
    # print('Initializing DF_PRIM_CPT')
    df_prim_cpt = pdb.read_excel(f'{ROOT_DIR}/inputs/{SPREAD_SHEET}', dtype=str, sheet_name=SHEET_NAME_PRIMCPT,
                                 header=8)
    # print('column names', df_prim_cpt.head())
    df_prim_cpt = df_prim_cpt.dropna(subset=[COL_PROC_CD, 'SvcType'])
    df_prim_cpt = df_prim_cpt.sort_values(by=['business', 'SvcType', 'SvcSubType', COL_PROC_CD])
    return df_prim_cpt


def _load_cpt_ranking_dict() -> Dict[str, CptRanking]:
    df = _init_prim_cpt()
    df = df.sort_values(by=[COL_PROC_CD, COL_RANK])
    cpt_ranking_entries = {}
    for index, row in df.iterrows():
        cpt_code = row.get(COL_PROC_CD)
        if not cpt_code:
            continue
        cpt_ranking = CptRanking(
            cpt_code=cpt_code,
            cpt_desc=row.get('CPT_Desc'),
            service_type=row.get('SvcType'),
            service_sub_type=row.get('SvcSubType'),
            business=row.get('business'),
            ranking=int(row.get(COL_RANK))
        )
        cpt_ranking_entries[cpt_code] = cpt_ranking

    return cpt_ranking_entries


class ProcedureCodes:
    DF_PRIM_CPT = _init_prim_cpt()

    def __init__(self, base_id: str):
        self.base_id = base_id

    def read_prim_cpt(self) -> Markup:
        """
        Each entry must have a unique id, otherwise the treeview
        :return: Markup
        """
        old_business = None
        svc_types = []
        old_svc_type = None
        svc_sub_types = []
        old_svc_sub_type = None
        proc_cds = []
        old_proc_cd = None
        businesses = []
        for index, row in self.DF_PRIM_CPT.iterrows():
            new_proc_cd = row.get(COL_PROC_CD).strip()
            if not MLAP_DICT.get(new_proc_cd):
                # skip codes that are not under consideration
                continue
            new_business = row.get('business').strip()
            new_svc_type = row.get('SvcType').strip()
            new_svc_sub_type = row.get('SvcSubType').strip()
            # print('code found', index, new_business, new_svc_type, new_svc_sub_type, new_proc_cd)

            if old_business == new_business:
                if old_svc_type == new_svc_type:
                    if old_svc_sub_type == new_svc_sub_type:
                        if old_proc_cd == new_proc_cd:
                            pass
                        else:
                            old_proc_cd = new_proc_cd
                            proc_cds.append(self._proc_cd_leaf(index, new_proc_cd))
                    else:
                        old_svc_sub_type = new_svc_sub_type
                        old_proc_cd = new_proc_cd
                        proc_cds = []
                        svc_sub_types.append(self._svc_sub_types_branch(index, new_svc_sub_type, proc_cds))
                        proc_cds.append(self._proc_cd_leaf(index, new_proc_cd))
                else:
                    old_svc_type = new_svc_type
                    old_svc_sub_type = new_svc_sub_type
                    old_proc_cd = new_proc_cd
                    svc_sub_types = []
                    proc_cds = []
                    svc_types.append(self._svc_types_branch(index, new_svc_type, svc_sub_types))
                    svc_sub_types.append(self._svc_sub_types_branch(index, new_svc_sub_type, proc_cds))
                    proc_cds.append(self._proc_cd_leaf(index, new_proc_cd))
            else:
                old_business = new_business
                old_svc_type = new_svc_type
                old_svc_sub_type = new_svc_sub_type
                old_proc_cd = new_proc_cd
                svc_types = []
                svc_sub_types = []
                proc_cds = []
                businesses.append(self._businesses_branch(index, new_business, svc_types))
                svc_types.append(self._svc_types_branch(index, new_svc_type, svc_sub_types))
                svc_sub_types.append(self._svc_sub_types_branch(index, new_svc_sub_type, proc_cds))
                proc_cds.append(self._proc_cd_leaf(index, new_proc_cd))

        return Markup(businesses)

    def _businesses_branch(self, index, name, children: list):
        return {'id': f'{self.base_id}-b-{index}', 'name': name, 'children': children}

    def _svc_types_branch(self, index, name, children: list):
        return {'id': f'{self.base_id}-bst-{index}', 'name': name, 'children': children}

    def _svc_sub_types_branch(self, index, name, children: list):
        return {'id': f'{self.base_id}-bstsst-{index}', 'name': name, 'children': children}

    def _proc_cd_leaf(self, index, proc_cd) -> dict:
        cpt_entry = MLAP_DICT.get(proc_cd)
        return {'id': f'{self.base_id}-proc_cd-{index}', 'name': f'{proc_cd} {cpt_entry.cpt_desc}',
                'choice': 'approve',
                'min_value': cpt_entry.cpt_min_confidence_level
                }


MLAP_DICT = _load_mlap_dict()
CPT_RANKING_DICT = _load_cpt_ranking_dict()
CPT_LOOKUP_DICT = _load_cpt_codes()

if __name__ == '__main__':
    print(CPT_LOOKUP_DICT)
    # print(CPT_LOOKUP_DICT.get('95806').total_cost())
    # print(CPT_RANKING_DICT)
    # print(CPT_RANKING_DICT.get('95806'))

    # print(MLAP_DICT)
    # my_cpt_entry = MLAP_DICT.get('95806')
    # print('my mlap code', my_cpt_entry)
    # procedure_codes = ProcedureCodes('xlss')
    # print(procedure_codes.read_prim_cpt())
