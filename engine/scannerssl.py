def _process_ssl_request(self, template_id, template_info, request_config, target_url):
        paths = request_config.get("path", []) # TODO : Strip this to just domain name in case any path exists 
        matchers_config = request_config.get("matchers", [])
        for path in paths:
            url = path.replace("{{BaseURL}}", target_url).strip("/")
            try:
                response = requests.get(url, verify=True)
                if response.url.startswith("https://"):
                    return {
                        "template_id": template_id,
                        "name": template_info.get("name"),
                        "author": template_info.get("author"),
                        "severity": template_info.get("severity"),
                        "url": url,
                        "status_code": response.status_code,
                        "matched": "Flase", # As a postive result
                    }
                else:
                    return {
                        "template_id": template_id,
                        "name": template_info.get("name"),
                        "author": template_info.get("author"),
                        "severity": template_info.get("severity"),
                        "url": url,
                        "status_code": response.status_code,
                        "matched": "True", # As a negetive result
                    }
            except requests.exceptions.SSLError:
                return {
                        "template_id": template_id,
                        "name": template_info.get("name"),
                        "author": template_info.get("author"),
                        "severity": template_info.get("severity"),
                        "url": url,
                        "status_code": response.status_code,
                        "matched": "True", # As a negetive result
                    }
            except requests.exceptions.RequestException as e:
                print("The request was errored out ", str(e))
