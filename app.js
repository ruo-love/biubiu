const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");
// 设置你的仓库路径
const repoPath = "./";
const time = "2024 1/9 17.52";
// 更新仓库
const updateRepo = () => {
  try {
    // 进入仓库目录
    process.chdir(repoPath);
    // 执行git pull命令
    execSync("git pull origin master");
    console.log("代码拉取成功！");                                                                                                                                          
    //更新package.json 中的updateTime 字段
    const packageJsonPath = path.resolve(__dirname, "./package.json");
    const packageJson = require(packageJsonPath);
    packageJson.updateTime = new Date().toLocaleString();
    // 写入package.json
    fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
    console.log("updateTime 更新成功！");
    // push 到远程仓库
    execSync("git add .");
    execSync('git commit -m "update"');
    execSync("git push origin main");
    console.log("远程仓库更新成功！");
  } catch (error) {
    console.error("仓库更新失败：", error.message);
  }
};

updateRepo();
