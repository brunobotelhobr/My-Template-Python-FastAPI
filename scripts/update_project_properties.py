"""Do project properties update."""
import toml  # type: ignore
import yaml  # type: ignore

# Loads TOML file.
with open('pyproject.toml', 'r') as file:  # pylint: disable=w1514
    data = toml.load(file)

# Print Banner
print("----------------------------------------------------------------")
print("Current project properties:")
print("----------------------------------------------------------------")
print(f"   name: {data['tool']['poetry']['name']}")
print(f"   version: {data['tool']['poetry']['version']}")
print(f"   license: {data['tool']['poetry']['license']}")
print(f"   description: {data['tool']['poetry']['description']}")
print(f"   authors: {data['tool']['poetry']['authors']}")
print(f"   maintainers: {data['tool']['poetry']['maintainers']}")
print(f"   readme: {data['tool']['poetry']['readme']}")
print(f"   packages: {data['tool']['poetry']['packages']}")
print(f"   repository: {data['tool']['poetry']['repository']}")
print(f"   homepage: {data['tool']['poetry']['homepage']}")
print(f"   keywords: {data['tool']['poetry']['keywords']}")
print(f"   docker-context: {data['tool']['taskipy']['variables']['docker-context']}")  # pylint: disable=line-too-long
print(f"   docs-branch: {data['tool']['taskipy']['variables']['docs-branch']}")  # pylint: disable=line-too-long
print("----------------------------------------------------------------")
print("Type new values for the project properties or press enter to keet the actual value:")  # pylint: disable=line-too-long
print("----------------------------------------------------------------")

# Read a value form user
awnsers = dict()
name = input("   name :")
if name != "":
    awnsers["name"] = name
version = input("   version :")
if version != "":
    awnsers["version"] = version
lic = input("   license :")
if lic != "":
    awnsers["license"] = lic
description = input("   description :")
if description != "":
    awnsers["description"] = description
authors = input("   authors :")
if authors != "":
    awnsers["authors"] = authors
maintainers = input("   maintainers :")
if maintainers != "":
    awnsers["maintainers"] = maintainers
readme = input("   readme :")
if readme != "":
    awnsers["readme"] = readme
packages = input("   packages :")
if packages != "":
    awnsers["packages"] = packages
repository = input("   repository :")
if repository != "":
    awnsers["repository"] = repository
homepage = input("   homepage :")
if homepage != "":
    awnsers["homepage"] = homepage
keywords = input("   keywords :")
if keywords != "":
    awnsers["keywords"] = keywords
docker_context = input("   docker-context :")
if docker_context != "":
    awnsers["docker-context"] = docker_context
docs_branch = input("   docs-branch :")
if docs_branch != "":
    awnsers["docs-branch"] = docs_branch

# Open toml file to write and update the values
with open('pyproject.toml', 'r+') as file:  # pylint: disable=w1514
    data = toml.load(file)
    for key, value in awnsers.items():
        if key in data['tool']['poetry']:
            data['tool']['poetry'][key] = value
        if key in data['tool']['taskipy']['variables']:
            data['tool']['taskipy']['variables'][key] = value       
    # Save the file
    file.seek(0)
    toml.dump(data, file)
    file.truncate()

# Open yaml file to write and update the values
with open('mkdocs.yml', 'r+',) as file:  # pylint: disable=w1514
    data = yaml.load(file, Loader=yaml.FullLoader)
    for key, value in awnsers.items():
        if key in data:
            data[key] = value
    # Save the file
    file.seek(0)
    yaml.dump(data, file)
    file.truncate()
