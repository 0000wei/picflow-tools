#!/usr/bin/env bash
# ===========================================================================
# PicEte - init.sh
# 生命周期启动脚本：让新会话 Agent 快速进入状态
# ===========================================================================
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_NAME="PicEte"
ONLINE_URL="https://picete.com"

# ── 颜色 ──
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  ${PROJECT_NAME} - Project Init${NC}"
echo -e "${CYAN}  线上地址: ${ONLINE_URL}${NC}"
echo -e "${CYAN}  项目路径: ${PROJECT_DIR}${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

# ── 检查关键文件是否存在 ──
echo -e "${YELLOW}[文件健康检查]${NC}"
MISSING_ANY=false
for f in README.md STRUCTURE-RULES.md AGENTS.md PROGRESS.md Makefile feature_list.json; do
    if [ -f "${PROJECT_DIR}/${f}" ]; then
        echo -e "  ${GREEN}✓${NC} ${f}"
    else
        echo -e "  ${RED}✗ WARNING: ${f} 不存在${NC}"
        MISSING_ANY=true
    fi
done
if [ "$MISSING_ANY" = true ]; then
    echo -e "  ${YELLOW}⚠  部分文件缺失，建议先创建补齐${NC}"
fi
echo ""

# ── Git 最近提交 ──
echo -e "${YELLOW}[最近 Git 提交]${NC}"
if git -C "${PROJECT_DIR}" rev-parse --git-dir > /dev/null 2>&1; then
    git -C "${PROJECT_DIR}" log --oneline -5
else
    echo -e "  ${RED}不是 Git 仓库${NC}"
fi
echo ""

# ── Git 未提交变更 ──
echo -e "${YELLOW}[未提交变更]${NC}"
if git -C "${PROJECT_DIR}" rev-parse --git-dir > /dev/null 2>&1; then
    STATUS=$(git -C "${PROJECT_DIR}" status --short)
    if [ -z "$STATUS" ]; then
        echo -e "  ${GREEN}干净，无未提交修改${NC}"
    else
        echo "$STATUS"
    fi
else
    echo -e "  ${RED}不是 Git 仓库${NC}"
fi
echo ""

# ── 提示 ──
echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  💡 提示：请先阅读 AGENTS.md 再开始工作${NC}"
echo -e "${CYAN}  （如果 AGENTS.md 缺失，跳过此步骤）${NC}"
echo -e "${CYAN}============================================${NC}"
