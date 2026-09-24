"""Structured logging tests for Router routing decisions. No model weights required."""
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from laya.router import Router  # noqa: E402

PASS, FAIL = [], []


def check(name, cond):
    if cond:
        PASS.append(name)
    else:
        FAIL.append(name)


def test_route_emits_info_log():
    logger = logging.getLogger("laya")
    records = []

    class _ListHandler(logging.Handler):
        def emit(self, record):
            records.append(record)

    handler = _ListHandler()
    handler.setLevel(logging.INFO)
    old_level = logger.level
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    try:
        r = Router()
        decision = r.route(
            {"body": "I was charged twice, please refund."},
            {"dept": {"type": "choice", "instructions": "Which team?",
                      "criteria": {"billing": None, "tech": None}}},
        )
        check("route returns decision", decision.model in ("english", "multilingual", "typed-decisions"))
        info_msgs = [rec.getMessage() for rec in records if rec.levelno >= logging.INFO]
        check("at least one info log", len(info_msgs) >= 1)
        check(
            "log mentions model",
            any(decision.model in m for m in info_msgs),
        )
        check(
            "log mentions routed",
            any("routed to" in m for m in info_msgs),
        )
    finally:
        logger.removeHandler(handler)
        logger.setLevel(old_level)


if __name__ == "__main__":
    test_route_emits_info_log()
    print("PASS: %d" % len(PASS))
    for n in PASS:
        print("  ok  %s" % n)
    if FAIL:
        print("FAIL: %d" % len(FAIL))
        for n in FAIL:
            print("  FAIL %s" % n)
        sys.exit(1)
    print("all logging tests passed")
