# kaos

The kaos core is contained within the backend, allowing users to **leverage flexible language agnostic data pipelines.** 

### Build

The most effective way to build the backend for development is with kaos [CLI](../cli/README.md).

1. Deploy a local cluster ([Docker Desktop](../infrastructure/docker/README.md))

```bash
kaos build -c DOCKER -vf
```

2. Make desired changes to the backend (i.e. development)

3. Re-deploy the local cluster **but** only the changes will be "built" (i.e. the new backend image)
```bash
kaos build -c DOCKER -vf
```

4. Kill the existing backend pod in kubernetes to force the pull policy on a new pod
```bash
kubectl get pod -l app=kaos-backend -o jsonpath="{.items[0].metadata.name}" | xargs -I {} kubectl delete pod {}
```

##
### Usage

The backend exposes a JSON-based API. For instance, you can create a workspace with the following call.

```bash
curl -X POST http://localhost:80/workspace/local
{
  "build_notebook": null,
  "build_serve": null,
  "build_train": null
}
```

See the full [API documentation](https://ki-labs.gitbook.io/kaos/api-reference-1) for more information.

##
### Structure

The application is divided into **four** layers.

- Module `routes`
  - The outermost layer that specifies the REST API of the backend and leaves all the processing tocontrollers. It handles everything HTTP-specific, marshals exceptions into responses.
- Module `controllers`
  - It contains all the high-level business logic of the application.
- Module `services`
  - It encapsulates all low-level mechanics and exposes an abstracted interface, so that the controllers manipulate with kaos-specific concepts without any low-level logic.
- Module `clients`
  - A thin wrapper over [Pachyderm](https://pachyderm.io/) internal storage and pipeline clients. It organizes access to Pachyderms' subsystems, decodes the responses and provides error handling.
  
##
### Testing

Standardized testing of the CLI consists of [pytest](https://docs.pytest.org/en/latest/) and [tox](https://tox.readthedocs.io/en/latest/). All significant functionality must come with test coverage. Please run tox within an isolated Docker environment using the supplied make file.

```bash
make test-unit-docker
```
