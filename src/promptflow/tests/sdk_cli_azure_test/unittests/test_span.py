import pytest

from promptflow._sdk.entities._trace import Span as SpanEntity
from promptflow.azure._storage.cosmosdb.span import Span


@pytest.mark.unittest
class TestSpan:
    FAKE_CREATED_BY = {"oid": "fake_oid"}
    FAKE_COLLECTION_ID = "fake_collection_id"
    FAKE_TRACE_ID = "0xacf2291a630af328da8fabd6bf49f653"
    FAKE_SPAN_ID = "0x9ded7ce65d5f7775"

    def test_to_dict(self):
        span = Span(
            SpanEntity(
                name="test",
                context={
                    "trace_id": self.FAKE_TRACE_ID,
                    "span_id": self.FAKE_SPAN_ID,
                },
                kind="test",
                parent_span_id="test",
                start_time="test",
                end_time="test",
                status={},
                attributes={},
                events=[],
                links=[],
                resource={},
                span_type=None,
                session_id=None,
            ),
            collection_id=self.FAKE_COLLECTION_ID,
            created_by=self.FAKE_CREATED_BY,
        )
        assert span.to_dict() == {
            "name": "test",
            "kind": "test",
            "parent_id": "test",
            "start_time": "test",
            "end_time": "test",
            "context": {
                "trace_id": self.FAKE_TRACE_ID,
                "span_id": self.FAKE_SPAN_ID,
            },
            "id": self.FAKE_SPAN_ID,
            "collection_id": "fake_collection_id",
            "created_by": {"oid": "fake_oid"},
        }

        span = Span(
            SpanEntity(
                name="test",
                context={
                    "trace_id": self.FAKE_TRACE_ID,
                    "span_id": self.FAKE_SPAN_ID,
                },
                kind="test",
                parent_span_id="test",
                start_time="test",
                end_time="test",
                status={},
                attributes={"line_run_id": "test_line_run_id"},
                events=[],
                links=[],
                resource={},
                span_type=None,
                session_id="test_session_id",
            ),
            collection_id=self.FAKE_COLLECTION_ID,
            created_by=self.FAKE_CREATED_BY,
        )
        assert span.to_dict() == {
            "name": "test",
            "kind": "test",
            "parent_id": "test",
            "start_time": "test",
            "end_time": "test",
            "attributes": {"line_run_id": "test_line_run_id"},
            "partition_key": "test_session_id",
            "context": {
                "trace_id": self.FAKE_TRACE_ID,
                "span_id": self.FAKE_SPAN_ID,
            },
            "id": self.FAKE_SPAN_ID,
            "partition_key": "test_session_id",
            "collection_id": "fake_collection_id",
            "created_by": {"oid": "fake_oid"},
        }

    def test_event_path(self):
        span = Span(
            SpanEntity(
                name="test",
                context={
                    "trace_id": self.FAKE_TRACE_ID,
                    "span_id": self.FAKE_SPAN_ID,
                },
                kind="test",
                parent_span_id="test",
                start_time="test",
                end_time="test",
                status={},
                attributes={},
                events=[],
                links=[],
                resource={},
                span_type=None,
                session_id=None,
            ),
            collection_id=self.FAKE_COLLECTION_ID,
            created_by=self.FAKE_CREATED_BY,
        )

        assert (
            span._event_path(1)
            == f".promptflow/.trace/{self.FAKE_COLLECTION_ID}/{self.FAKE_TRACE_ID}/{self.FAKE_SPAN_ID}/1"
        )
