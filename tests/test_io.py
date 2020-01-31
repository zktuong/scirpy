from sctcrpy import read_10x_vdj, read_tracer
from sctcrpy._util import _is_na, _is_false
import numpy as np
import pytest


def test_read_10x_example():
    anndata = read_10x_vdj("tutorial/example_data/10x/all_contig_annotations.json")


def test_read_tracer_example():
    anndata = read_tracer("tutorial/example_data/tracer/tracer_100")


def test_read_10x():
    anndata = read_10x_vdj("tests/data/10x/all_contig_annotations.json")
    obs = anndata.obs
    # this has `is_cell=false` and should be filtered out
    assert "AAACCTGAGACCTTTG-1" not in anndata.obs_names
    assert obs.shape[0] == 2
    cell1 = obs.iloc[0, :]
    cell2 = obs.iloc[1, :]

    assert cell1.name == "AAACCTGAGACCTTTG-2"
    assert cell1["TRB_1_cdr3"] == "CASSPPSQGLSTGELFF"
    assert (
        cell1["TRB_1_cdr3_nt"] == "TGTGCCAGCTCACCACCGAGCCAGGGCCTTTCTACCGGGGAGCTGTTTTTT"
    )
    assert cell1["TRB_1_cdr3_len"] == len("CASSPPSQGLSTGELFF")
    assert cell1["TRB_1_junction_ins"] == 4 + 7
    assert cell1["TRB_1_expr"] == 1
    assert cell1["TRB_1_v_gene"] == "TRBV18"
    assert cell1["TRB_1_d_gene"] == "TRBD1"
    assert cell1["TRB_1_j_gene"] == "TRBJ2-2"
    assert cell1["TRB_1_c_gene"] == "TRBC2"
    assert _is_false(cell1["multi_chain"])
    assert np.all(
        _is_na(
            cell1[["TRA_1_cdr3", "TRB_2_cdr3", "TRA_1_cdr3_len", "TRA_1_junction_ins"]]
        )
    )

    assert cell2.name == "AAACCTGAGTACGCCC-1"
    assert cell2["TRA_1_cdr3"] == "CAMRVGGSQGNLIF"
    assert cell2["TRA_2_cdr3"] == "CATDAKDSNYQLIW"
    assert cell2["TRA_1_expr"] == 9
    assert cell2["TRA_2_expr"] == 4
    assert np.all(_is_na(cell2[["TRB_1_cdr3", "TRB_2_cdr3"]]))
    assert cell2["TRA_1_junction_ins"] == 4
    assert cell2["TRA_2_junction_ins"] == 4


def test_read_tracer():
    with pytest.raises(IOError):
        anndata = read_tracer("sctcrpy")

    anndata = read_tracer("tests/data/tracer")
    assert "cell1" in anndata.obs_names and "cell2" in anndata.obs_names
    assert anndata.obs.shape[0] == 2

    cell1 = anndata.obs.loc["cell1", :]
    cell2 = anndata.obs.loc["cell2", :]

    assert cell1.name == "cell1"
    assert cell1["TRA_1_cdr3"] == "AESTGTSGTYKYI"
    assert cell1["TRA_1_cdr3_len"] == len("AESTGTSGTYKYI")
    assert cell1["TRB_1_cdr3"] == "ASSYSVSRSGELF"
    assert cell1["TRB_1_cdr3_len"] == len("ASSYSVSRSGELF")

    assert cell2.name == "cell2"
    assert cell2["TRA_1_cdr3"] == "ALSEAEGGSEKLV"
    assert cell2["TRA_1_cdr3_len"] == len("ALSEAEGGSEKLV")
    assert cell2["TRB_1_cdr3"] == "ASSYNRGPGGTQY"
    assert cell2["TRB_1_cdr3_len"] == len("ASSYNRGPGGTQY")
    assert cell2["TRB_1_j_gene"] == "TRBJ2-5"
