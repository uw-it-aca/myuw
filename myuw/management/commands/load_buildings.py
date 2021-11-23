# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from uw_space import Facilities
from myuw.models import CampusBuilding
from myuw.util.settings import get_cronjob_recipient, get_cronjob_sender

BUILDING_CODES = [
    "AAB",
    "AAC",
    "ACC",
    "ADA",
    "ADI",
    "ADL",
    "ADMC",
    "ADS",
    "AER",
    "ALB",
    "AND",
    "ARC",
    "ART",
    "ATG",
    "ATS",
    "AU",
    "AZ",
    "BAG",
    "BB",
    "BFB",
    "BGH",
    "BHA",
    "BHS",
    "BIOE",
    "BLD",
    "BMM",
    "BNS",
    "BOW",
    "BRA",
    "BRY",
    "CAR",
    "CC1",
    "CCC",
    "CDA",
    "CDH",
    "CHB",
    "CHCL",
    "CHL",
    "CHSB",
    "CHSC",
    "CLK",
    "CMA",
    "CMU",
    "CNH",
    "COL",
    "CP",
    "CRB",
    "CSE",
    "CSE2",
    "CSH",
    "CYB",
    "DEM",
    "DEN",
    "DISC",
    "DOU",
    "DRC",
    "DSC",
    "ECC",
    "ECE",
    "EDP",
    "EGA",
    "EGL",
    "EHD",
    "EK",
    "ELB",
    "ESB",
    "EXED",
    "FAC",
    "FLK",
    "FRH",
    "FSH",
    "FTR",
    "GA1",
    "GA2",
    "GA3",
    "GA4",
    "GAB",
    "GDR",
    "GLB",
    "GLD",
    "GNOM",
    "GRB",
    "GTH",
    "GUA",
    "GUG",
    "GWN",
    "GWP",
    "HAG",
    "HCK",
    "HGT",
    "HH",
    "HHL",
    "HLL",
    "HMC",
    "HND",
    "HNS",
    "HPT",
    "HRC",
    "HS4",
    "HSA",
    "HSAA",
    "HSB",
    "HSBB",
    "HSC",
    "HSD",
    "HSE",
    "HSF",
    "HSG",
    "HSH",
    "HSI",
    "HSJ",
    "HSK",
    "HSRR",
    "HST",
    "HUB",
    "HUT",
    "IC2",
    "ICH",
    "ICT",
    "IMA",
    "IPF",
    "ISA",
    "JHA",
    "JHN",
    "JOY",
    "KEY",
    "KIN",
    "KIR",
    "KNE",
    "LA1",
    "LAN",
    "LAVC",
    "LAVM",
    "LAVN",
    "LAVP",
    "LAVQ",
    "LAVR",
    "LAVS",
    "LAVT",
    "LAVU",
    "LAVV",
    "LAVW",
    "LAVX",
    "LAVY",
    "LAW",
    "LB1",
    "LB2",
    "LBA",
    "LBH",
    "LEW",
    "LOW",
    "LSH",
    "LSS",
    "MAR",
    "MAT",
    "MCC",
    "MCM",
    "MCR",
    "MDS",
    "MEB",
    "MGH",
    "MKZ",
    "MLR",
    "MNY",
    "MOL",
    "MOR",
    "MSB",
    "MSS",
    "MUE",
    "MUS",
    "NAN",
    "NHS",
    "NLB",
    "NMH",
    "NPC",
    "NPS",
    "NRB",
    "NTC",
    "OBS",
    "OCE",
    "OCN",
    "ODB",
    "OR1",
    "OR2",
    "OSS",
    "OTB",
    "OTS",
    "OTT",
    "OUG",
    "PAA",
    "PAB",
    "PAR",
    "PAT",
    "PCAR",
    "PCH",
    "PDL",
    "PHT",
    "PL1",
    "PL2",
    "PLT",
    "PNK",
    "PO2",
    "PO3",
    "PO4",
    "PO5",
    "PO6",
    "POB",
    "PRO",
    "PSB",
    "PSC",
    "PSV",
    "PWR",
    "RAI",
    "RAX",
    "REC",
    "ROB",
    "RSN",
    "RTB",
    "SAV",
    "SCA",
    "SCB",
    "SCC",
    "SCD",
    "SCI",
    "SCJ",
    "SCK",
    "SCL",
    "SCM",
    "SGS",
    "SHA",
    "SIG",
    "SLA",
    "SLB",
    "SLC",
    "SMI",
    "SMZ",
    "SNO",
    "SOCC",
    "SSGC",
    "STD",
    "SUZ",
    "SWS",
    "TER",
    "TGB",
    "THO",
    "TLB",
    "TPS",
    "TSB",
    "UDB",
    "UFA",
    "UFB",
    "UHF",
    "UMCC",
    "UMEB",
    "UMEE",
    "UMNN",
    "UMNW",
    "UMSE",
    "UMSP",
    "UMSS",
    "UMSW",
    "UW1",
    "UW2",
    "UWBB",
    "UWMC",
    "UWTA",
    "UWTC",
    "UWTO",
    "UWTS",
    "UWTT",
    "UWY",
    "WAC",
    "WCG",
    "WCL",
    "WFS",
    "WG",
    "WHT",
    "WIL",
    "WLA",
    "WNX",
    "WPH",
    "WRS",
    "WSB",
    "WSG",
    "WSP",
    "ZAK"
]
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Update building table"

    def add_arguments(self, parser):
        parser.add_argument(
            "-l", "--initial-load", action="store_true", dest="load",
            default=False,
            help="operation")

    def handle(self, *args, **options):
        count = 0
        messages = []
        space = Facilities()

        if options.get('load'):
            CampusBuilding.objects.all().delete()
            for bcode in BUILDING_CODES:
                try:
                    fac_objs = space.search_by_code(bcode)
                    if fac_objs and len(fac_objs):
                        bdg = CampusBuilding.upd_building(fac_objs[0])
                        logger.info("Loaded {}".format(bdg))
                        count += 1
                except Exception as ex:
                    msg = {"Load building": bcode, "err": ex}
                    logger.error(msg)
                    messages.append("\n{}".format(msg))
            logger.info(
                "Loaded {}/{} building codes".format(
                    count, len(BUILDING_CODES)))
        else:
            builds_in_db = CampusBuilding.objects.all()
            for bdg in builds_in_db:
                try:
                    fac = space.search_by_number(bdg.number)
                    if not bdg.no_change(fac):
                        updated_bdg = CampusBuilding.upd_building(fac)
                        logger.info("Updated {}".format(updated_bdg))
                        count += 1
                except Exception as ex:
                    msg = {"Load building": bdg, "err": ex}
                    logger.error(msg)
                    messages.append("\n{}".format(msg))

        if len(messages):
            send_mail(
                "Update CampusBuilding",
                "\n".join(messages),
                "{}@uw.edu".format(get_cronjob_sender()),
                ["{}@uw.edu".format(get_cronjob_recipient())])
