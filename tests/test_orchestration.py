import pytest

from orchestration import pipeline


class FakeSpark:
    pass


def test_run_pipeline_executes_stages_in_order(monkeypatch):
    calls = []

    monkeypatch.setattr(
        pipeline,
        "run_bronze_pipeline",
        lambda spark: calls.append("BRONZE"),
    )
    monkeypatch.setattr(
        pipeline,
        "run_silver_pipeline",
        lambda spark: calls.append("SILVER"),
    )
    monkeypatch.setattr(
        pipeline,
        "run_gold_pipeline",
        lambda spark: calls.append("GOLD"),
    )

    spark = FakeSpark()
    pipeline.run_pipeline(spark=spark)

    assert calls == ["BRONZE", "SILVER", "GOLD"]


def test_run_pipeline_stops_after_stage_failure(monkeypatch):
    calls = []

    def fail_silver(spark):
        calls.append("SILVER")
        raise RuntimeError("silver failed")

    monkeypatch.setattr(
        pipeline,
        "run_bronze_pipeline",
        lambda spark: calls.append("BRONZE"),
    )
    monkeypatch.setattr(pipeline, "run_silver_pipeline", fail_silver)
    monkeypatch.setattr(
        pipeline,
        "run_gold_pipeline",
        lambda spark: calls.append("GOLD"),
    )

    with pytest.raises(RuntimeError, match="silver failed"):
        pipeline.run_pipeline(spark=FakeSpark())

    assert calls == ["BRONZE", "SILVER"]
