const { execSync } = require('child_process');
const path = require('path');

// 设置你的仓库路径
const repoPath = './';

// 更新仓库
const updateRepo = () => {
  try {
    // 进入仓库目录
    process.chdir(repoPath);

    // 执行git pull命令
    execSync('git pull origin main');

    console.log('仓库更新成功！');
  } catch (error) {
    console.error('仓库更新失败：', error.message);
  }
};

updateRepo();
