"""Tests for go.apps.jsbox.metrics."""

from vxsandbox.resources import SandboxCommand

from vumi.tests.helpers import VumiTestCase

from vxsandbox.resources.metrics import (
    MetricEvent, MetricEventError, MetricsResource)


class TestMetricEvent(VumiTestCase):

    SUM = MetricEvent.AGGREGATORS['sum']

    def test_create(self):
        ev = MetricEvent('mystore', 'foo', 2.0, self.SUM)
        self.assertEqual(ev.store, 'mystore')
        self.assertEqual(ev.metric, 'foo')
        self.assertEqual(ev.value, 2.0)
        self.assertEqual(ev.agg, self.SUM)

    def test_eq(self):
        ev1 = MetricEvent('mystore', 'foo', 1.5, self.SUM)
        ev2 = MetricEvent('mystore', 'foo', 1.5, self.SUM)
        self.assertEqual(ev1, ev2)

    def test_neq(self):
        ev1 = MetricEvent('mystore', 'foo', 1.5, self.SUM)
        ev2 = MetricEvent('mystore', 'bar', 1.5, self.SUM)
        self.assertNotEqual(ev1, ev2)

    def test_from_command(self):
        ev = MetricEvent.from_command({'store': 'mystore', 'metric': 'foo',
                                       'value': 1.5, 'agg': 'sum'})
        self.assertEqual(ev, MetricEvent('mystore', 'foo', 1.5, self.SUM))

    def test_bad_store(self):
        self.assertRaises(MetricEventError, MetricEvent.from_command, {
                'store': 'foo bar', 'metric': 'foo', 'value': 1.5,
                'agg': 'sum'})

    def test_bad_type_store(self):
        self.assertRaises(MetricEventError, MetricEvent.from_command, {
                'store': {}, 'metric': 'foo', 'value': 1.5,
                'agg': 'sum'})

    def test_bad_metric(self):
        self.assertRaises(MetricEventError, MetricEvent.from_command, {
                'store': 'mystore', 'metric': 'foo bar', 'value': 1.5,
                'agg': 'sum'})

    def test_bad_type_metric(self):
        self.assertRaises(MetricEventError, MetricEvent.from_command, {
                'store': 'mystore', 'metric': {}, 'value': 1.5,
                'agg': 'sum'})

    def test_missing_metric(self):
        self.assertRaises(MetricEventError, MetricEvent.from_command, {
                'store': 'mystore', 'value': 1.5, 'agg': 'sum'})

    def test_bad_value(self):
        self.assertRaises(MetricEventError, MetricEvent.from_command, {
                'store': 'mystore', 'metric': 'foo', 'value': 'abc',
                'agg': 'sum'})

    def test_bad_type_value(self):
        self.assertRaises(MetricEventError, MetricEvent.from_command, {
                'store': 'mystore', 'metric': 'foo', 'value': {},
                'agg': 'sum'})

    def test_missing_value(self):
        self.assertRaises(MetricEventError, MetricEvent.from_command, {
                'store': 'mystore', 'metric': 'foo', 'agg': 'sum'})

    def test_bad_agg(self):
        self.assertRaises(MetricEventError, MetricEvent.from_command, {
                'store': 'mystore', 'metric': 'foo', 'value': 1.5,
                'agg': 'foo'})

    def test_bad_type_agg(self):
        self.assertRaises(MetricEventError, MetricEvent.from_command, {
                'store': 'mystore', 'metric': 'foo', 'value': 1.5,
                'agg': {}})

    def test_missing_agg(self):
        self.assertRaises(MetricEventError, MetricEvent.from_command, {
                'store': 'mystore', 'metric': 'foo', 'value': 1.5})


class TestMetricsResource(VumiTestCase):

    SUM = MetricEvent.AGGREGATORS['sum']

    def setUp(self):
        self.dummy_api = object()

    def check_reply(self, reply, cmd, success):
        self.assertEqual(reply['reply'], True)
        self.assertEqual(reply['cmd_id'], cmd['cmd_id'])
        self.assertEqual(reply['success'], success)

    def check_publish(self, store, metric, value, agg):
        self.app_worker.publish_account_metric.assert_called_once_with(
            self.conversation.user_account.key, store, metric, value, agg)

    def check_not_published(self):
        self.assertFalse(self.app_worker.publish_account_metric.called)

    def test_handle_fire(self):
        """
        """

    def _test_error(self, cmd, expected_error):
        reply = self.resource.handle_fire(self.dummy_api, cmd)
        self.check_reply(reply, cmd, False)

    def test_handle_fire_error(self):
        """
        """

    def test_non_ascii_metric_name_error(self):
        """
        """