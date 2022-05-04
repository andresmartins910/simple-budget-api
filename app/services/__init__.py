def verify_required_keys(data, trusted_keys):

    err_missing_key = {
                    "required_keys": trusted_keys,
                    "sended_keys": list(data.keys())
                }

    for key in trusted_keys:
        if key not in data.keys():
            raise KeyError(err_missing_key)


def verify_allowed_keys(data, allowed_keys):

    err_missing_key = {
                    "allowed_keys": allowed_keys,
                    "sended_keys": list(data.keys())
                }

    for key in data.keys():
        if key not in allowed_keys:
            raise KeyError(err_missing_key)