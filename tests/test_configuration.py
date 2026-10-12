"""
The deployment configuration (docker/configuration/config.json, passed with --conf) is laid
over the packaged default (src/nodenorm/config/config.default.json), so it holds only the
settings the deployment changes.
"""

from nodenorm.namespace import merge_configuration


def test_merge_keeps_the_keys_an_override_leaves_out():
    base = {"elasticsearch": {"ES_HOST": "http://localhost:9200", "ES_ARGS": {"sniff": False, "request_timeout": 60}}}
    override = {"elasticsearch": {"ES_HOST": "http://es:9200", "ES_ARGS": {"request_timeout": 5}}}

    assert merge_configuration(base, override) == {
        "elasticsearch": {"ES_HOST": "http://es:9200", "ES_ARGS": {"sniff": False, "request_timeout": 5}}
    }
    assert base["elasticsearch"]["ES_HOST"] == "http://localhost:9200", "the base must not be modified"


def test_merge_replaces_lists_whole():
    merged = merge_configuration({"URLS": ["^/$", "^/status$"]}, {"URLS": ["^/webapp"]})
    assert merged == {"URLS": ["^/webapp"]}
