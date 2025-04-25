"""
Python model 'Dijken_en_Natuur_v4_small.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import if_then_else
from pysd.py_backend.statefuls import NonNegativeInteg, Integ
from pysd import Component

__pysd_version__ = "3.14.2"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 120,
    "time_step": lambda: 1 / 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="INITIAL TIME", units="Months", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="FINAL TIME", units="Months", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="TIME STEP", units="Months", comp_type="Constant", comp_subtype="Normal"
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


@component.add(
    name="SAVEPER",
    units="Months",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The save time step for the simulation.
    """
    return __data["time"].saveper()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="capacity of ripening",
    units="m3 sediment/Months",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "area_of_ripening": 1,
        "thickness": 1,
        "months": 2,
        "ripening_sediment": 1,
    },
)
def capacity_of_ripening():
    return area_of_ripening() * thickness() * months() - ripening_sediment() * months()


@component.add(
    name="sediment-to-clay factor",
    units="m3_clay/m3_sediment",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sedimenttoclay_factor():
    return 1 / 3


@component.add(
    name="months", units="Per Month", comp_type="Constant", comp_subtype="Normal"
)
def months():
    return 1


@component.add(
    name="cost savings of ripening",
    units="EUR/m3_sediment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cost_of_disposal": 1,
        "cost_to_ripen": 1,
        "price_of_clay_in_sediment_terms": 1,
    },
)
def cost_savings_of_ripening():
    return cost_of_disposal() - (cost_to_ripen() - price_of_clay_in_sediment_terms())


@component.add(
    name="maximum fixable dykes",
    units="m3_clay/Months",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_clay_for_fixing_dykes": 1, "months_per_year": 1},
)
def maximum_fixable_dykes():
    return annual_clay_for_fixing_dykes() / months_per_year()


@component.add(
    name="months per year",
    units="Months/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def months_per_year():
    return 12


@component.add(
    name="annual dredging",
    units="m3_sediment/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"shipping_dredging_demand": 1},
)
def annual_dredging():
    return shipping_dredging_demand()


@component.add(
    name="area of ripening",
    units="m2_sediment",
    comp_type="Constant",
    comp_subtype="Normal",
)
def area_of_ripening():
    return 35000


@component.add(
    name="thickness", units="m_sediment", comp_type="Constant", comp_subtype="Normal"
)
def thickness():
    return 0.3


@component.add(
    name="annual clay for fixing dykes",
    units="m3_clay/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def annual_clay_for_fixing_dykes():
    return 310000


@component.add(
    name="shipping dredging demand",
    units="m3_sediment/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def shipping_dredging_demand():
    return 3000000


@component.add(
    name="portion of dykes that are fixed",
    units="Dimensionless",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fixed_green_dyke": 1, "months": 1, "maximum_fixable_dykes": 1},
)
def portion_of_dykes_that_are_fixed():
    return fixed_green_dyke() * months() / (maximum_fixable_dykes() * 12 * 6)


@component.add(
    name="k constant",
    units="Dimensionless",
    comp_type="Constant",
    comp_subtype="Normal",
)
def k_constant():
    return 1


@component.add(
    name="societal uptake",
    units="Dimensionless",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "portion_of_dykes_that_are_fixed": 2,
        "minimum_societal_uptake": 2,
        "k_constant": 1,
    },
)
def societal_uptake():
    return if_then_else(
        portion_of_dykes_that_are_fixed() > 0,
        lambda: float(
            np.maximum(
                1 / (1 + (1 / portion_of_dykes_that_are_fixed() - 1) ** k_constant()),
                minimum_societal_uptake(),
            )
        ),
        lambda: minimum_societal_uptake(),
    )


@component.add(
    name="annual sediment input 1",
    units="m3 sediment/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def annual_sediment_input_1():
    return 4000000


@component.add(
    name="minimum societal uptake",
    units="Dimensionless",
    comp_type="Constant",
    comp_subtype="Normal",
)
def minimum_societal_uptake():
    return 0.01


@component.add(
    name="demand for ripening",
    units="m3 sediment/Months",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "unfixed_dykes": 1,
        "societal_uptake": 1,
        "sedimenttoclay_factor": 1,
        "months": 1,
        "capacity_of_ripening": 1,
    },
)
def demand_for_ripening():
    return float(
        np.minimum(
            unfixed_dykes() * societal_uptake() / sedimenttoclay_factor() * months(),
            capacity_of_ripening(),
        )
    )


@component.add(
    name="cost to ripen",
    units="EUR/m3_sediment",
    comp_type="Constant",
    comp_subtype="Normal",
)
def cost_to_ripen():
    """
    20 is made up. It is the price to get it from estuary to ripening place. Agreed price of ripened sediment is 15.


    10.75 is the opbrengst of 1m3 klei+rest. Rounded to 10.50. Divide by 3 to get it in terms of sediment to get 3.50
    https://pure.rug.nl/ws/portalfiles/portal/113204879/MCKBA_evaluatie_slibketens_Sijtsma_et_al_RUG_final_9.pdf
    """
    return 1.04


@component.add(
    name="cost of disposal",
    units="EUR/m3_sediment",
    comp_type="Constant",
    comp_subtype="Normal",
)
def cost_of_disposal():
    """
    https://pure.rug.nl/ws/portalfiles/portal/113204879/MCKBA_evaluatie_slibketens_Sijtsma_et_al_RUG_final_9.pdf
    """
    return 1.04


@component.add(
    name="ripening cheaper?",
    units="Dimensionless",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cost_savings_of_ripening": 1},
)
def ripening_cheaper():
    return if_then_else(cost_savings_of_ripening() > 0, lambda: 1, lambda: 0)


@component.add(
    name="price of clay in sediment terms",
    units="EUR/m3_sediment",
    comp_type="Constant",
    comp_subtype="Normal",
)
def price_of_clay_in_sediment_terms():
    """
    5EUR/m3 in sediment terms. From report: 15EUR/m3 clay, and 3:1 sediment-clay ratio
    """
    return 5


@component.add(
    name="load from river/sea",
    units="m3_sediment/Months",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_sediment_input_1": 1, "months_per_year": 1},
)
def load_from_riversea():
    return float(np.maximum(annual_sediment_input_1() / months_per_year(), 0))


@component.add(
    name="dredging",
    units="m3_sediment/Months",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"estuary_sediment": 1, "annual_dredging": 1, "months_per_year": 1},
)
def dredging():
    return float(
        np.maximum(
            if_then_else(
                estuary_sediment() < 3000000 / 12,
                lambda: 0,
                lambda: annual_dredging() / months_per_year(),
            ),
            0,
        )
    )


@component.add(
    name="disposal",
    units="m3_sediment/Months",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cost_savings_of_ripening": 1,
        "dredged_sediment": 2,
        "months": 2,
        "transport_to_ripening": 1,
    },
)
def disposal():
    return float(
        np.maximum(
            if_then_else(
                cost_savings_of_ripening() < 0,
                lambda: dredged_sediment() * months(),
                lambda: dredged_sediment() * months() - transport_to_ripening(),
            ),
            0,
        )
    )


@component.add(
    name="transport to ripening",
    units="m3_sediment/Months",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cost_savings_of_ripening": 1,
        "dredged_sediment": 1,
        "demand_for_ripening": 1,
        "months": 1,
    },
)
def transport_to_ripening():
    """
    this one only works with the ambition being fulfilled
    """
    return float(
        np.maximum(
            if_then_else(
                cost_savings_of_ripening() >= 0,
                lambda: float(
                    np.minimum(dredged_sediment() * months(), demand_for_ripening())
                ),
                lambda: 0,
            ),
            0,
        )
    )


@component.add(
    name="ripening",
    units="m3_sediment/Months",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ripening():
    return float(np.maximum(0, 0))


@component.add(
    name="apply on this dyke",
    units="m3_clay/Months",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"available_clay": 1, "months": 1},
)
def apply_on_this_dyke():
    return float(np.maximum(available_clay() * months(), 0))


@component.add(
    name="fixing dykes",
    units="m3_clay/Months",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"apply_on_this_dyke": 1, "maximum_fixable_dykes": 1},
)
def fixing_dykes():
    return float(
        np.maximum(float(np.minimum(apply_on_this_dyke(), maximum_fixable_dykes())), 0)
    )


@component.add(
    name="apply on other dykes",
    units="m3_clay/Months",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"unfixed_dykes": 1, "available_clay": 1, "months": 1},
)
def apply_on_other_dykes():
    return float(
        np.maximum(
            if_then_else(
                unfixed_dykes() <= 0, lambda: available_clay() * months(), lambda: 0
            ),
            0,
        )
    )


@component.add(
    name="estuary sediment",
    units="m3_sediment",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_estuary_sediment": 1},
    other_deps={
        "_integ_estuary_sediment": {
            "initial": {},
            "step": {"load_from_riversea": 1, "dredging": 1},
        }
    },
)
def estuary_sediment():
    return _integ_estuary_sediment()


_integ_estuary_sediment = NonNegativeInteg(
    lambda: load_from_riversea() - dredging(), lambda: 0, "_integ_estuary_sediment"
)


@component.add(
    name="dredged sediment",
    units="m3_sediment",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_dredged_sediment": 1},
    other_deps={
        "_integ_dredged_sediment": {
            "initial": {},
            "step": {"dredging": 1, "disposal": 1, "transport_to_ripening": 1},
        }
    },
)
def dredged_sediment():
    return _integ_dredged_sediment()


_integ_dredged_sediment = NonNegativeInteg(
    lambda: dredging() - disposal() - transport_to_ripening(),
    lambda: 0,
    "_integ_dredged_sediment",
)


@component.add(
    name="ripening sediment",
    units="m3_sediment",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ripening_sediment": 1},
    other_deps={
        "_integ_ripening_sediment": {
            "initial": {},
            "step": {"transport_to_ripening": 1, "ripening": 1},
        }
    },
)
def ripening_sediment():
    """
    Need to fix capacity, ideally connect it to a variable somehow


    """
    return _integ_ripening_sediment()


_integ_ripening_sediment = Integ(
    lambda: transport_to_ripening() - ripening(), lambda: 0, "_integ_ripening_sediment"
)


@component.add(
    name="available clay",
    units="m3_clay",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_available_clay": 1},
    other_deps={
        "_integ_available_clay": {
            "initial": {},
            "step": {"ripening": 1, "apply_on_this_dyke": 1, "apply_on_other_dykes": 1},
        }
    },
)
def available_clay():
    return _integ_available_clay()


_integ_available_clay = NonNegativeInteg(
    lambda: ripening() - apply_on_this_dyke() - apply_on_other_dykes(),
    lambda: 0,
    "_integ_available_clay",
)


@component.add(
    name="fixed green dyke",
    units="m3_clay",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_fixed_green_dyke": 1},
    other_deps={
        "_integ_fixed_green_dyke": {"initial": {}, "step": {"fixing_dykes": 1}}
    },
)
def fixed_green_dyke():
    return _integ_fixed_green_dyke()


_integ_fixed_green_dyke = NonNegativeInteg(
    lambda: fixing_dykes(), lambda: 0, "_integ_fixed_green_dyke"
)


@component.add(
    name="unfixed dykes",
    units="m3_clay",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_unfixed_dykes": 1},
    other_deps={"_integ_unfixed_dykes": {"initial": {}, "step": {"fixing_dykes": 1}}},
)
def unfixed_dykes():
    """
    For entire BGD (12.5km) we need 280-350,000m3 of gerijpteklei per year

    We will use 310,000m3 per year for 6 years for 12.5km
    """
    return _integ_unfixed_dykes()


_integ_unfixed_dykes = NonNegativeInteg(
    lambda: -fixing_dykes(), lambda: 310000 * 6, "_integ_unfixed_dykes"
)


@component.add(
    name="clay for other dykes",
    units="m3_clay",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_clay_for_other_dykes": 1},
    other_deps={
        "_integ_clay_for_other_dykes": {
            "initial": {},
            "step": {"apply_on_other_dykes": 1},
        }
    },
)
def clay_for_other_dykes():
    return _integ_clay_for_other_dykes()


_integ_clay_for_other_dykes = NonNegativeInteg(
    lambda: apply_on_other_dykes(), lambda: 0, "_integ_clay_for_other_dykes"
)
