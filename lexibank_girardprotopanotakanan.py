import attr
import pathlib
from collections import defaultdict
from clldutils.misc import slug
from lingpy import Wordlist
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Lexeme, Concept
from pylexibank import FormSpec


@attr.s
class CustomConcept(Concept):
    Proto_ID = attr.ib(default=None)


@attr.s
class CustomLexeme(Lexeme):
    ProtoForm = attr.ib(default=None)
    ConceptInSource = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "girardprotopanotakanan"
    concept_class = CustomConcept
    lexeme_class = CustomLexeme
    form_spec = FormSpec(separators=",~")

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        args.log.info("added sources")

        # add concepts
        concepts = defaultdict()
        for concept in self.etc_dir.read_csv("concepts.tsv", delimiter="\t", dicts=True):
            idx = slug(concept["GLOSS"])
            args.writer.add_concept(
                ID=idx,
                Name=concept["GLOSS"],
                Concepticon_ID=concept["CONCEPTICON_ID"],
                Concepticon_Gloss=concept["CONCEPTICON_GLOSS"],
                Proto_ID=concept["PROTO_ID"]
                )

            concepts[concept["GLOSS"]] = idx

        args.log.info("added concepts")

        # Proto-Pano Takana
        languages = args.writer.add_languages(lookup_factory="ID")
        args.log.info("added languages")

        data = Wordlist(str(self.raw_dir.joinpath("raw.tsv")))

        # add data
        for (
            idx,
            proto_set,
            proto_form,
            proto_concept,
            doculect,
            concept,
            value,
            comment
        ) in pb(
            data.iter_rows(
                "proto_set",
                "proto_form",
                "proto_concept",
                "doculect",
                "concept",
                "value",
                "comment",
            ),
            desc="cldfify"
        ):
            if doculect in languages:
                args.writer.add_forms_from_value(
                    Language_ID=languages[doculect],
                    Parameter_ID=concepts[(proto_concept.replace('**', '').replace('*', ''))],
                    Value=value.strip(),
                    ProtoForm=proto_form,
                    Comment=comment,
                    Cognacy=proto_set,
                    ConceptInSource=concept
                )
