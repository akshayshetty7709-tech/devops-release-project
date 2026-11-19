# Project: Ship a Versioned App (Git + Tags + Docker + CI/CD)

You will take a tiny Python web app from first commit to a tagged, containerized release,
then break it and roll back, like a real DevOps team.

Needs: Git, a GitHub account, Docker (optional locally), Docker Hub account (for Phase 6).

## Phase 1: Repo setup
1. Unzip, then `cd devops-release-project`
2. `git init -b main`
3. Create the workflow folder and move the file:
   `mkdir -p .github/workflows` (it is already placed if you unzipped as given)
4. `git add .` then `git commit -m "chore: initial project"`
5. Create an EMPTY repo on GitHub under YOUR account, then:
   `git remote add origin https://github.com/<your-username>/devops-demo.git`
   `git push -u origin main` (use a Personal Access Token as the password)

## Phase 2: Branch, PR, merge
1. `git checkout -b feature/PROJ-1-add-version-endpoint`
2. Edit `app.py`: add a `/version` route returning `{"version": VERSION}`
3. Add a test for it in `test_app.py`, run `python3 -m unittest -v`
4. Commit: `feat: add /version endpoint`
5. Push, open a Pull Request, wait for the CI "test" job to go green, squash merge

## Phase 3: Create a conflict on purpose
1. Branch A: change the default port in `app.py` to 9090
2. Branch B (from main): change it to 7070
3. Merge A, then merge B, resolve the conflict, commit

## Phase 4: First release with tags
1. `git checkout main && git pull`
2. `git tag -a v1.0.0 -m "First release"`
3. `git push origin v1.0.0`

## Phase 5: Docker image tagging (local)
```
docker build --build-arg APP_VERSION=1.0.0 -t devops-demo:1.0.0 .
docker tag devops-demo:1.0.0 devops-demo:1.0
docker tag devops-demo:1.0.0 devops-demo:$(git rev-parse --short HEAD)
docker run -p 8080:8080 devops-demo:1.0.0
curl localhost:8080
docker images devops-demo
```
Check that three tags point to the same IMAGE ID.

## Phase 6: CI/CD pipeline
1. On Docker Hub, create an access token
2. GitHub repo > Settings > Secrets and variables > Actions, add:
   `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`
3. Push a new tag: `v1.1.0` (after merging the /version feature)
4. Watch the Actions tab: test, then build and push
5. Confirm tags `1.1.0`, `1.1`, and a SHA tag appear on Docker Hub

## Phase 7: Break it and roll back
1. Merge a bad change (e.g. make `/health` return status 500)
2. Tag `v1.2.0` and let the pipeline publish it
3. Roll back by running the previous image: `docker run -p 8080:8080 <user>/devops-demo:1.1.0`
4. Fix Git history safely: `git revert <bad-commit>` (or `git revert -m 1 <merge>` for a merge), PR, merge

## Phase 8: Hotfix
1. `git checkout -b hotfix/health-fix v1.1.0`
2. Fix, commit, PR into main
3. Tag `v1.2.1` (patch) and verify the pipeline publishes it

## Done checklist
- [ ] Commits follow Conventional Commits (feat:, fix:, chore:)
- [ ] No direct pushes to main (enable branch protection in repo settings)
- [ ] Tags v1.0.0, v1.1.0, v1.2.0, v1.2.1 exist
- [ ] Docker Hub shows multiple tags per release
- [ ] You performed one revert and one rollback
- [ ] `git log --oneline --graph --decorate --all` looks like a real project history

## Stretch goals
- Add CODEOWNERS and require 1 approval on PRs
- Add a Trivy scan step to ci.yml before pushing
- Auto-create a GitHub Release from each tag
