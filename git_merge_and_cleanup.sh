#!/usr/bin/env bash
# Se estiver no zsh, reexecuta em bash para evitar problemas de arrays/prompt
if [ -n "${ZSH_VERSION-}" ]; then
  exec bash "$0" "$@"
fi

set -euo pipefail

# ---------- util ----------
run() { echo "+ $*"; "$@"; }

# Busca indice (1-based) de um nome dentro do array BRANCHES; retorna 0 se nao achar
index_of_branch() {
  local name="$1"
  local i=0
  for b in "${BRANCHES[@]}"; do
    i=$((i+1))
    if [ "$b" = "$name" ]; then
      echo "$i"
      return 0
    fi
  done
  echo 0
}

# ---------- fetch ----------
echo "[INFO] Fetching all branches from remote..."
run git fetch --all

# ---------- montar lista (local + remota) ----------
echo "[INFO] Building branch list (local + remote)..."
BRANCHES=()

# Locais (curto, ordenado)
while read -r b; do
  [ -z "$b" ] && continue
  BRANCHES+=("$b")
done < <(git branch --format='%(refname:short)' | sort -u)

# Remotas reais: apenas refs em refs/remotes/origin/*, ignorando origin/HEAD
while read -r rb; do
  # rb vem como "origin/<nome>"
  name="${rb#origin/}"
  # ignora HEAD e qualquer anomalia
  { [ "$name" = "HEAD" ] || [ -z "$name" ] || [ "$name" = "origin" ]; } && continue
  # adiciona se ainda nao estiver na lista
  if ! printf '%s\0' "${BRANCHES[@]}" | grep -Fxqz -- "$name"; then
    BRANCHES+=("$name")
  fi
done < <(git for-each-ref --format='%(refname:short)' 'refs/remotes/origin/*' | sort -u)

if [ "${#BRANCHES[@]}" -eq 0 ]; then
  echo "[ERROR] No branches found."
  exit 1
fi

# Mostrar numeradas com marcador (local/remote)
echo "[INFO] Available branches:"
idx=1
for b in "${BRANCHES[@]}"; do
  if git show-ref --verify --quiet "refs/heads/$b"; then
    suffix="(local)"
  else
    suffix="(remote)"
  fi
  printf "  [%d] %s %s\n" "$idx" "$b" "$suffix"
  idx=$((idx+1))
done

# ---------- default da SOURCE: ultima remota atualizada ----------
LAST_REMOTE_BRANCH="$(
  git for-each-ref --sort=-committerdate --format='%(refname:short)' 'refs/remotes/origin/*' \
  | grep -v '^origin/HEAD$' \
  | sed 's|^origin/||' \
  | grep -v '^origin$' \
  | head -n 1 || true
)"

DEFAULT_SRC_INDEX=1
if [ -n "${LAST_REMOTE_BRANCH:-}" ]; then
  found_idx="$(index_of_branch "$LAST_REMOTE_BRANCH")"
  if [ "$found_idx" -gt 0 ]; then
    DEFAULT_SRC_INDEX="$found_idx"
  fi
fi

# ---------- default da TARGET: branch atual ----------
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
DEFAULT_TGT_INDEX="$(index_of_branch "$CURRENT_BRANCH")"
# se nao achar a atual na lista (raro), tenta 'main'
if [ "$DEFAULT_TGT_INDEX" -eq 0 ]; then
  DEFAULT_TGT_INDEX="$(index_of_branch main)"
fi
# fallback para 1 se ainda 0
[ "$DEFAULT_TGT_INDEX" -eq 0 ] && DEFAULT_TGT_INDEX=1
# evita defaults iguais
if [ "$DEFAULT_TGT_INDEX" -eq "$DEFAULT_SRC_INDEX" ]; then
  DEFAULT_TGT_INDEX=1
  [ "$DEFAULT_TGT_INDEX" -eq "$DEFAULT_SRC_INDEX" ] && DEFAULT_TGT_INDEX=2
  [ "$DEFAULT_TGT_INDEX" -gt "${#BRANCHES[@]}" ] && DEFAULT_TGT_INDEX=1
fi

# ---------- escolher SOURCE ----------
echo -n "Enter the number of the SOURCE branch to merge FROM [default: ${DEFAULT_SRC_INDEX}]: "
read -r SRC_NUM
SRC_NUM=${SRC_NUM:-$DEFAULT_SRC_INDEX}
if ! [[ "$SRC_NUM" =~ ^[0-9]+$ ]] || [ "$SRC_NUM" -lt 1 ] || [ "$SRC_NUM" -gt "${#BRANCHES[@]}" ]; then
  echo "[ERROR] Invalid selection for SOURCE."
  exit 1
fi
SRC_BRANCH="${BRANCHES[$((SRC_NUM-1))]}"
echo "[INFO] SOURCE branch: $SRC_BRANCH"

# ---------- escolher TARGET ----------
echo -n "Enter the number of the TARGET branch to merge INTO [default: ${DEFAULT_TGT_INDEX}]: "
read -r TGT_NUM
TGT_NUM=${TGT_NUM:-$DEFAULT_TGT_INDEX}
if ! [[ "$TGT_NUM" =~ ^[0-9]+$ ]] || [ "$TGT_NUM" -lt 1 ] || [ "$TGT_NUM" -gt "${#BRANCHES[@]}" ]; then
  echo "[ERROR] Invalid selection for TARGET."
  exit 1
fi
TGT_BRANCH="${BRANCHES[$((TGT_NUM-1))]}"
echo "[INFO] TARGET branch: $TGT_BRANCH"

if [ "$SRC_BRANCH" = "$TGT_BRANCH" ]; then
  echo "[ERROR] SOURCE and TARGET cannot be the same."
  exit 1
fi

# ---------- ssh agent (opcional) ----------
eval "$(ssh-agent -s)" >/dev/null 2>&1 || true
ssh-add ~/.ssh/id_rsa >/dev/null 2>&1 || true
ssh -T git@github.com || true  # mensagem "no shell access" e esperada

# ---------- commit de seguranca ----------
if [[ -n $(git status --porcelain) ]]; then
  echo "[INFO] Local changes detected. Performing automatic commit..."
  run git add .
  run git commit -m "Automatic backup before merge"
else
  echo "[INFO] No local changes pending."
fi

# ---------- preparar TARGET ----------
echo "[INFO] Switching to TARGET: $TGT_BRANCH"
if git show-ref --verify --quiet "refs/heads/$TGT_BRANCH"; then
  run git switch "$TGT_BRANCH"
else
  if git show-ref --verify --quiet "refs/remotes/origin/$TGT_BRANCH"; then
    run git switch -c "$TGT_BRANCH" --track "origin/$TGT_BRANCH"
  else
    run git switch -c "$TGT_BRANCH"
  fi
fi
run git pull --ff-only origin "$TGT_BRANCH" || true
run git push -u origin "$TGT_BRANCH" || true

# ---------- garantir SOURCE local ----------
if git show-ref --verify --quiet "refs/heads/$SRC_BRANCH"; then
  echo "[INFO] SOURCE exists locally."
else
  if git show-ref --verify --quiet "refs/remotes/origin/$SRC_BRANCH"; then
    echo "[INFO] Creating local SOURCE from origin/$SRC_BRANCH"
    run git fetch origin "$SRC_BRANCH"
    run git branch "$SRC_BRANCH" "origin/$SRC_BRANCH"
  else
    echo "[ERROR] SOURCE branch not found locally or on origin: $SRC_BRANCH"
    exit 1
  fi
fi

# ---------- merge ----------
echo "[INFO] Merging '$SRC_BRANCH' into '$TGT_BRANCH'"
set +e
git merge "$SRC_BRANCH" --no-edit
merge_status=$?
set -e

if [ "$merge_status" -ne 0 ]; then
  echo "[ERROR] Merge has conflicts. Resolve them, then run:"
  echo "  git diff --name-only --diff-filter=U"
  echo "  edit files, then: git add -A && git commit --no-edit && git push"
  exit 1
fi

run git status --short
run git push

# ---------- limpeza local (opcional) ----------
echo "[INFO] Optional cleanup of non-protected local branches..."
current_branch="$(git rev-parse --abbrev-ref HEAD)"
git branch --format='%(refname:short)' \
  | awk -v cur="$current_branch" -v a="$TGT_BRANCH" -v b="$SRC_BRANCH" '
      $0!=cur && $0!=a && $0!=b &&
      index($0,"main")==0 && index($0,"edf")==0 && index($0,"iae")==0 &&
      index($0,"ita")==0  && index($0,"ufabc")==0
    ' \
  | while read -r delb; do
      [ -z "$delb" ] && continue
      echo "[INFO] Deleting local branch: $delb"
      git branch -D "$delb" || true
    done

git branch | cat

# ---------- limpeza remota (segura) ----------
echo "[INFO] Optional cleanup of non-protected remote branches..."
git for-each-ref --format='%(refname:short)' 'refs/remotes/origin/*' \
  | grep -v '^origin/HEAD$' \
  | sed 's|^origin/||' \
  | grep -v '^origin$' \
  | awk -v a="$TGT_BRANCH" -v b="$SRC_BRANCH" '
      NF && $0!=a && $0!=b &&
      index($0,"main")==0 && index($0,"edf")==0 && index($0,"iae")==0 &&
      index($0,"ita")==0  && index($0,"ufabc")==0
    ' \
  | xargs -r -I {} sh -c '
      echo "[INFO] Deleting remote branch: {}"
      git push origin --delete "{}" || true
    '

echo "[INFO] Done."
git branch -r | cat
git status
