"""Transparent phrase lexicons for Sydney Protocol signal detection.

These are conservative heuristics. They surface possible review signals; they
never prove intent, manipulation, corruption, harm, illegality, or truth.
"""

from __future__ import annotations

from .models import Language, Severity

SIGNAL_DEFINITIONS = {
    "pressure": {
        Language.EN: ("Pressure language", "The input may push someone toward fast agreement or compliance.", Severity.REVIEW),
        Language.NL: ("Druktaal", "De tekst kan iemand richting snelle instemming of gehoorzaamheid duwen.", Severity.REVIEW),
    },
    "boundary": {
        Language.EN: ("Boundary concern", "The input may blur choice, privacy, consent, or personal limits.", Severity.REVIEW),
        Language.NL: ("Grenssignaal", "De tekst kan keuze, privacy, toestemming of persoonlijke grenzen vervagen.", Severity.REVIEW),
    },
    "evidence_gap": {
        Language.EN: ("Evidence gap", "The input makes a claim without enough visible evidence, source, date, or mechanism.", Severity.REVIEW),
        Language.NL: ("Bewijsgat", "De tekst doet een claim zonder genoeg zichtbaar bewijs, bron, datum of mechanisme.", Severity.REVIEW),
    },
    "authority_overclaim": {
        Language.EN: ("Authority overclaim", "The input may claim more authority, certainty, or control than it explains.", Severity.WARNING),
        Language.NL: ("Autoriteitsoverclaim", "De tekst kan meer gezag, zekerheid of controle claimen dan wordt uitgelegd.", Severity.WARNING),
    },
    "safety": {
        Language.EN: ("Safety concern", "The input may involve urgency, harm, threat, isolation, or unsafe escalation.", Severity.WARNING),
        Language.NL: ("Veiligheidssignaal", "De tekst kan haast, schade, dreiging, isolatie of onveilige escalatie bevatten.", Severity.WARNING),
    },
    "corruption_pressure": {
        Language.EN: ("Integrity / corruption-risk signal", "The input may show opacity, concentrated benefit, favoritism, weak oversight, or accountability gaps.", Severity.WARNING),
        Language.NL: ("Integriteits- / corruptierisico-signaal", "De tekst kan ondoorzichtigheid, geconcentreerd voordeel, vriendjespolitiek, zwak toezicht of verantwoordingsgaten tonen.", Severity.WARNING),
    },
    "repair_opportunity": {
        Language.EN: ("Repair opportunity", "The input may benefit from clarification, accountability, apology, appeal, or calmer wording.", Severity.INFO),
        Language.NL: ("Herstelmogelijkheid", "De tekst kan baat hebben bij verduidelijking, verantwoording, excuses, bezwaarroute of rustiger taal.", Severity.INFO),
    },
}

SIGNAL_LIMITATIONS = {
    Language.EN: {
        "pressure": "This does not prove coercion or intent; context may change the reading.",
        "boundary": "This does not prove a boundary violation; it flags a possible review point.",
        "evidence_gap": "This does not prove the claim is false; it flags missing visible support.",
        "authority_overclaim": "This does not prove illegitimate authority; it flags a possible overclaim.",
        "safety": "This is not emergency triage or diagnosis; seek immediate local help if there is danger.",
        "corruption_pressure": "This does not allege corruption; it flags integrity-risk patterns for review.",
        "repair_opportunity": "This is a suggestion area, not an obligation or judgment.",
    },
    Language.NL: {
        "pressure": "Dit bewijst geen dwang of intentie; context kan de lezing veranderen.",
        "boundary": "Dit bewijst geen grensoverschrijding; het markeert een mogelijk reviewpunt.",
        "evidence_gap": "Dit bewijst niet dat de claim onwaar is; het markeert ontbrekende zichtbare onderbouwing.",
        "authority_overclaim": "Dit bewijst geen onrechtmatig gezag; het markeert een mogelijke overclaim.",
        "safety": "Dit is geen noodtriage of diagnose; zoek direct lokale hulp als er gevaar is.",
        "corruption_pressure": "Dit beschuldigt niet van corruptie; het markeert integriteitsrisicopatronen voor review.",
        "repair_opportunity": "Dit is een suggestiegebied, geen verplichting of oordeel.",
    },
}

PHRASES = {
    Language.EN: {
        "pressure": (
            "you must", "right now", "no choice", "trust me", "do not question", "don't question",
            "everyone knows", "if you cared", "prove it", "you have to", "immediately",
        ),
        "boundary": (
            "keep this secret", "nobody needs to know", "do not tell", "don't tell", "you owe me",
            "prove your loyalty", "between us", "do this for me", "do not share this",
        ),
        "evidence_gap": (
            "studies prove", "experts say", "it is obvious", "guaranteed", "proven safe", "verified safe",
            "scientifically proven", "no evidence needed", "everyone agrees", "clearly true",
        ),
        "authority_overclaim": (
            "only we can", "final decision", "certified truth", "we decide", "absolute authority",
            "no appeal", "non-negotiable", "officially true", "the only solution",
        ),
        "safety": (
            "threat", "harm", "kill", "hurt", "emergency", "danger", "unsafe", "blackmail", "extort",
            "retaliate", "punish you", "isolated", "do not contact anyone",
        ),
        "corruption_pressure": (
            "special access", "private arrangement", "no oversight", "favor", "kickback", "conflict of interest",
            "backroom", "under the table", "friends and family", "preferred vendor", "no audit",
        ),
        "repair_opportunity": (
            "sorry", "apologize", "misunderstanding", "clarify", "appeal", "review", "correct", "accountability",
        ),
    },
    Language.NL: {
        "pressure": (
            "je moet", "nu meteen", "geen keuze", "vertrouw me", "stel geen vragen", "iedereen weet",
            "als je om me gaf", "als je echt om me gaf", "bewijs het", "je hebt geen keuze", "onmiddellijk",
        ),
        "boundary": (
            "hou dit geheim", "houd dit geheim", "niemand hoeft dit te weten", "niet vertellen",
            "je bent me verschuldigd", "bewijs je loyaliteit", "tussen ons", "doe dit voor mij", "niet delen",
        ),
        "evidence_gap": (
            "onderzoek bewijst", "experts zeggen", "het is duidelijk", "gegarandeerd", "bewezen veilig",
            "geverifieerd veilig", "wetenschappelijk bewezen", "geen bewijs nodig", "iedereen is het eens",
        ),
        "authority_overclaim": (
            "alleen wij kunnen", "definitieve beslissing", "gecertificeerde waarheid", "wij bepalen",
            "absolute autoriteit", "geen bezwaar", "niet onderhandelbaar", "de enige oplossing",
        ),
        "safety": (
            "dreiging", "schade", "doden", "pijn doen", "noodgeval", "gevaar", "onveilig", "chantage",
            "afpersen", "wraak", "straffen", "isoleer", "neem met niemand contact op",
        ),
        "corruption_pressure": (
            "speciale toegang", "privéregeling", "geen toezicht", "gunst", "smeergeld", "belangenconflict",
            "achterkamertje", "onder tafel", "vrienden en familie", "voorkeursleverancier", "geen audit",
        ),
        "repair_opportunity": (
            "sorry", "excuses", "misverstand", "verduidelijken", "bezwaar", "review", "corrigeren", "verantwoording",
        ),
    },
}
