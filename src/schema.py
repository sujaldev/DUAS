from validators import domain, ipv4, ipv6


def is_valid_network_destination(field, value, error):
    # TODO: could support CIDR ranges later on
    is_domain = domain(value)
    is_ipv4 = ipv4(value)
    is_ipv6 = ipv6(value)
    if not (is_domain or is_ipv4 or is_ipv6):
        error(field, f"'{field}' is not a valid domain or ipv4/ipv6 address.")


# Ping Schema
ping_schema = {
    "retry_limit": {
        "type": "integer",
        "required": True,
        "coerce": int,
        "min": 1,
    }
}

# HTTP(s) Schema
http_schema = {
}

# Heartbeat Schema
heartbeat_schema = {
}

# Check-Method Schema
check_method_schema = {
    "ping": {
        "type": "dict",
        "nullable": True,
        "schema": ping_schema,
    },
    "http": {
        "type": "dict",
        "nullable": True,
        "schema": http_schema,
    },
    "https": {
        "type": "dict",
        "nullable": True,
        "schema": http_schema,
    },
    "heartbeat": {
        "type": "dict",
        "nullable": True,
        "schema": heartbeat_schema,
    },
}

# Meta Config Schema
meta_config_schema = {
    "log_level": {
        "type": "string",
    },
    "ping_retry_limit": {
        "type": "integer",
        "coerce": int,
    }
}

# Main Schema
schema = {
    "meta_config": {
        "type": "dict",
        "nullable": True,
        "schema": meta_config_schema,
    },
    "host_config": {
        "type": "dict",
        "keysrules": {
            "type": "string",
            "check_with": is_valid_network_destination,
        },
        "valuesrules": {
            "type": "dict",
            "schema": check_method_schema,
        }
    }
}
