# import requests
# import json

# # Charger les données du fichier JSON
# json_str = repo_conf.json

# data = json.loads(json_str)

# # Effectuer la requête POST vers l'API
# response = requests.post("https://example.com/api/update_release", json=data)

# # Vérifier le code de retour de la requête
# if response.status_code == 200:
#     print("La requête a été envoyée avec succès !")
# else:
#     print("Une erreur est survenue lors de l'envoi de la requête : ", response.text)

###################################################################
# ================================================================
##################################################################

import requests
import json

# Authentification avec un token d'accès
headers = {
    "Authorization": "token YOUR_ACCESS_TOKEN"
}

# Identifiant du repository
repo_owner = "owner"
repo_name = "repo"

# Identifiant de la release à mettre à jour
release_id = "1"

# Nouvelles informations pour la release et ses sous-composants
release_data = {
    "tag_name": "v2.0",
    "name": "Release 2.0",
    "body": "Description de la release 2.0",
    "draft": False,
    "prerelease": False,
    "assets": [
        {
            "name": "asset1.txt",
            "label": "Asset 1",
            "content_type": "text/plain",
            "data": "Contenu du fichier asset1.txt"
        },
        {
            "name": "asset2.txt",
            "label": "Asset 2",
            "content_type": "text/plain",
            "data": "Contenu du fichier asset2.txt"
        }
    ]
}

# Effectuer la requête PUT vers l'API GitHub
response = requests.put(f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/{release_id}", headers=headers, data=json.dumps(release_data))

# Vérifier le code de retour de la requête
if response.status_code == 200:
    print("La release a été mise à jour avec succès !")
else:
    print("Une erreur est survenue lors de la mise à jour de la release : ", response.text)

# ======================================================
# ======================================================

import requests
import json

class Release:
    def __init__(self, provider_email, bl, du, sc, fusionCAs, codePath, sub_component, gerritserver, project, branch, repo_name, actived, feature_validation, repo_type):
        self.provider_email = provider_email
        self.bl = bl
        self.du = du
        self.sc = sc
        self.fusionCAs = fusionCAs
        self.codePath = codePath
        self.sub_component = sub_component
        self.gerritserver = gerritserver
        self.project = project
        self.branch = branch
        self.repo_name = repo_name
        self.actived = actived
        self.feature_validation = feature_validation
        self.repo_type = repo_type

    def get_release_data(self):
        release_data = {
            "action": "api",
            "provider_email": self.provider_email,
            "data": [{
                "bl": self.bl,
                "du": self.du,
                "sc": self.sc,
                "fusionCAs": self.fusionCAs,
                "codePath": self.codePath,
                "sub_component": self.sub_component,
                "gerritserver": self.gerritserver,
                "project": self.project,
                "branch": self.branch,
                "repo_name": self.repo_name,
                "actived": self.actived,
                "feature_validation": self.feature_validation,
                "repo_type": self.repo_type
            }]
        }
        return release_data

    def update_release(self):
        headers = {'content-type': 'application/json'}
        url = 'http://your_api_url/update_release'
        release_data = self.get_release_data()
        response = requests.post(url, data=json.dumps(release_data), headers=headers)
        print(response.text)

if __name__ == '__main__':
    provider_email = "i_mn_5gsc_5g_sw_eng_ci_metrics_error@groups.nokia.com"
    bl = "MN RAN"
    du = "MN RAN L2"
    sc = "GNB"
    fusionCAs = "5G L2 HI;5G L2 LO;5G L2 PS;5G L3;5G L3 DU"
    codePath = {
        "SCT":"(.*?/(tickler|cpp_testsuites|sct|SCT|mct|MCT)|^l2_l3_test)/.*",
        "UT":".*?/((ut|UT|mt|MT|tst|TST)/.*|test_.*\\.py|.*_test\\.py)"
    }
    sub_component = {
        "uplane/L2-PS":"uplane/L2-PS/.*|uplane/sct/tickler/cpp_testsuites/l2ps/.*|uplane/sct/cpp_testsuites/fuse/stubs/.*|uplane/sct/cpp_testsuites/fuse/common/.*|uplane/sct/cpp_testsuites/fuse/testEnvironments/l2ps/.*",
        "uplane/L2-COMMON":"uplane/common/.*",
        "uplane/L2-HI":"uplane/L2-HI/.*",
        "uplane/L2-LO":"uplane/L2-LO/.*|uplane/sct/tickler/cpp_testsuites/l2lo/.*|uplane/sct/cpp_testsuites/fuse/stubs/.*|uplane/sct/cpp_testsuites/fuse/common/.*|"}

    gerritserver = "your_gerrit_server"
    project = "your_project"
    branch = "your_branch"
    repo_name = "your_repo_name"
    actived = "1"
    feature_validation = "0"
    repo_type = "git"
    release = Release(provider_email, bl, du, sc, fusionCAs, codePath, sub_component, gerritserver, project, branch, repo_name, actived, feature_validation, repo_type)
    release.update_release()

# =================================================================
# ===================================================================
import json
import requests

# Charge les données depuis le fichier JSON
with open('data.json', 'r') as f:
    data = json.load(f)

# Récupère les informations nécessaires depuis les données chargées
provider_email = data['provider_email']
gerritserver = data['gerritserver']
project = data['project']
repo_name = data['repo_name']
sub_components = data['sub_component']

# Récupère la liste des branches pour ce projet
url = f'https://{gerritserver}/a/projects/{project}/branches/'
response = requests.get(url)
branches = response.json()

# Parcourt chaque branche
for branch in branches:
    branch_name = branch['ref'].split('/')[-1]
    if branch_name not in data['branch']:
        # Si la branche n'existe pas déjà dans la liste des branches dans le fichier JSON
        # Ajoute la branche à la liste des branches dans le fichier JSON
        data['branch'].append(branch_name)
        print(f"Ajout de la branche {branch_name}")
        for component, regex in sub_components.items():
            # Met à jour les Sub_components pour cette nouvelle branche
            url = f'https://{gerritserver}/a/projects/{project}/branches/{branch_name}/ref-update'
            payload = {
                "command": "update",
                "ref": f"refs/heads/{branch_name}",
                "oldRev": "0000000000000000000000000000000000000000",
                "newRev": branch['revision'],
                "submodule": {
                    "action": "update",
                    "name": f"{repo_name}/{component}",
                    "submodule_gitlink": f"https://{gerritserver}/r/{repo_name}/{component}.git",
                    "submodule_refs": {
                        "fetch": f"+refs/heads/{branch_name}:refs/heads/{branch_name}",
                        "push": f"+refs/heads/{branch_name}:refs/heads/{branch_name}"
                    },
                    "paths": [regex]
                }
            }
            response = requests.post(url, auth=(provider_email, ''), json=payload)
            if response.status_code == 200:
                print(f"Sub_component {component} a été mis à jour pour la branche {branch_name}")
            else:
                print(f"Erreur lors de la mise à jour du Sub_component {component} pour la branche {branch_name}")
    
# Sauvegarde les données mises à jour dans le fichier JSON
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

# ================================================================================

import requests
import json

class ReleaseUpdater:
    def __init__(self, api_key, json_file):
        self.api_key = api_key
        with open(json_file) as f:
            self.config = json.load(f)

    def get_release_data(self):
        release_data = {}
        for release in self.config["data"]:
            bl = release["bl"]
            du = release["du"]
            sc = release["sc"]
            for branch in release["branch"]:
                if branch not in release_data:
                    release_data[branch] = {}
                if bl not in release_data[branch]:
                    release_data[branch][bl] = {}
                if du not in release_data[branch][bl]:
                    release_data[branch][bl][du] = {}
                if sc not in release_data[branch][bl][du]:
                    release_data[branch][bl][du][sc] = []
                release_data[branch][bl][du][sc].append(release)
        return release_data

    def update_sub_components(self, branch):
        release_data = self.get_release_data()
        for bl in release_data[branch]:
            for du in release_data[branch][bl]:
                for sc in release_data[branch][bl][du]:
                    sub_component = self.config["data"][0]["sub_component"]
                    sub_component_pattern = sub_component[sc]
                    for release in release_data[branch][bl][du][sc]:
                        code_path = release["codePath"]
                        code_path_pattern = code_path["SCT"]
                        url = f"https://{release['gerritserver']}/a/changes/?q=branch:{branch}+status:merged+project:{release['project']}+message:{release['provider_email']}+code_review_verified"
                        r = requests.get(url, headers={"Authorization": f"Bearer {self.api_key}"})
                        r.raise_for_status()
                        for change in r.json():
                            for file in change["revisions"][change["current_revision"]]["files"]:
                                if re.match(code_path_pattern, file):
                                    for sub_component_match in re.findall(sub_component_pattern, file):
                                        sub_component_path = sub_component_match.strip('/')
                                        if sub_component_path not in release_data[branch][bl][du]:
                                            release_data[branch][bl][du][sub_component_path] = []
                                        if release not in release_data[branch][bl][du][sub_component_path]:
                                            release_data[branch][bl][du][sub_component_path].append(release)

        # Update the config file with the new sub-components
        for release in self.config["data"]:
            bl = release["bl"]
            du = release["du"]
            sc = release["sc"]
            release["sub_component"] = {}
            for sub_component in release_data[branch][bl][du][sc]:
                release["sub_component"][sub_component] = sub_component_pattern
        with open(json_file, "w") as f:
            json.dump(self.config, f, indent=4)

if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    json_file = "release_config.json"
    updater = ReleaseUpdater(api_key, json_file)
    updater.update_sub_components("Rel/23_R3")

###========================================================

import requests
import json

class SubComponentUpdater:
    def __init__(self, api_url):
        self.api_url = api_url

    def update_sub_components(self, branch):
        data = {"branch": branch}

        # Send a POST request to the API endpoint
        response = requests.post(self.api_url, json=data)

        if response.status_code == 200:
            # Parse the response JSON
            response_data = json.loads(response.text)

            # Process the response data and update the sub-components accordingly
            # ...
        else:
            print("Error: API returned status code", response.status_code)

# Example usage
api_url = "https://example.com/api/update_sub_components"
updater = SubComponentUpdater(api_url)
updater.update_sub_components("my_new_branch")

########################################3
import requests
import json

url = "http://coop.int.net.nokia.com:3001/api/commits/config/repo_post"

# Charger les données depuis le fichier repo_conf.json
with open('repo_conf.json') as f:
    data = json.load(f)

# Envoyer la requête POST avec les données chargées
response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
print(response.status_code)

import requests
import json

url = "http://coop.int.net.nokia.com:3001/api/commits/config/repo_post"
headers = {'Content-Type': 'application/json'}
data = json.load(open('repo_conf.json'))

response = requests.post(url, headers=headers, json=data)

print(response.text)


