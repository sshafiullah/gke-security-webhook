import base64
import copy
import http
import json
import jsonpatch

from flask import Flask, jsonify, request
def mutate(request):
    """Used to invoke a cloud function that will apply pod security policies to newly created namespaces
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    spec = request.json["request"]["object"]
    modified_spec = copy.deepcopy(spec)

    if modified_spec["metadata"]["name"] == "testme" or modified_spec["metadata"]["name"] == "istio-addons":
      try:
          modified_spec["metadata"]["labels"]["pod-security.kubernetes.io/enforce"] = "privileged"
      except KeyError:
        pass
    else:
      try:
          modified_spec["metadata"]["labels"]["pod-security.kubernetes.io/enforce"] = "baseline"
          modified_spec["metadata"]["labels"]["pod-security.kubernetes.io/warn"] = "restricted"
      except KeyError:
        pass
    patch = jsonpatch.JsonPatch.from_diff(spec, modified_spec)
    return jsonify(
        {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "allowed": True,
                "uid": request.json["request"]["uid"],
                "patch": base64.b64encode(str(patch).encode()).decode(),
                "patchType": "JSONPatch",
            }
        }
    )

