package controller;

import gui.Home;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

public class SettingController {

    public SettingController(){}

    public static class ExecuteResult {
        private final int exitCode;
        private final String output;

        public int getExitCode() {
            return exitCode;
        }

        public String getOutput() {
            return output;
        }

        public ExecuteResult(int exitCode, String output) {
            this.exitCode = exitCode;
            this.output = output;
        }

        // getters...
    }

    public static ExecuteResult executeCommand(List<String> command, long timeout, TimeUnit timeUnit)
            throws IOException, InterruptedException, TimeoutException {

        ProcessBuilder pb = new ProcessBuilder(command);
        pb.redirectErrorStream(true);

        Process process = pb.start();

        try (InputStream is = process.getInputStream();
             BufferedReader reader = new BufferedReader(new InputStreamReader(is))) {

            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }

            if (!process.waitFor(timeout, timeUnit)) {
                process.destroyForcibly();
                throw new TimeoutException("Command timed out: " + command);
            }

            return new ExecuteResult(process.exitValue(), output.toString());
        }
    }

    /**
     * 启用开机自启动
     * @param appName 注册表中显示的名称（如"MyApp"）
     * @param appPath 程序的完整路径（如 "C:\MyApp\app.jar"）
     */
    public static void enableAutoStart(String appName, String appPath) {
        try {
            // 构造注册表命令
            ExecuteResult result = executeCommand(
                    Arrays.asList(
                            "reg",
                            "add",
                            "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                            "/v",
                            "\"" + appName + "\"",
                            "/t",
                            "REG_SZ",
                            "/d",
                            "\"" + appPath + "\"",
                            "/f"
                            ),
                    10, TimeUnit.SECONDS);
            Home.OUTPUT.append("已添加开机自启: " + appName);
        } catch (Exception e) {
            Home.OUTPUT.append(e.getMessage());
        }
    }

    /**
     * 禁用开机自启动
     * @param appName 注册表中的名称
     */
    public static void disableAutoStart(String appName) {
        try {
            // 构造注册表命令
            ExecuteResult result = executeCommand(
                    Arrays.asList(
                            "reg",
                            "delete",
                            "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                            "/v",
                            "\"" + appName + "\"",
                            "/f"
                    ),
                    10, TimeUnit.SECONDS);
            Home.OUTPUT.append("已移除开机自启: " + appName);
        } catch (Exception e) {
            Home.OUTPUT.append(e.getMessage());
        }
    }

    /**
     * 添加计划任务
     * @param taskName 计划任务中显示的名称（如"MyApp"）
     * @param exePath 程序的完整路径（如 "C:\MyApp\app.exe"）
     */
    @Deprecated
    public static void createTask(String taskName, String exePath) {
        try {
            // 计划任务
            String cmd = "schtasks /create /tn \"" + taskName + "\" " +
                    "/tr \"" + exePath + "\" /sc onlogon /rl HIGHEST";

            // 执行命令
            Runtime.getRuntime().exec(cmd);
            Home.OUTPUT.setText("已添加计划任务: " + taskName);
        } catch (IOException e) {
            Home.OUTPUT.setText("添加计划任务失败: " + e.getMessage());
        }
    }

    /**
     * 删除计划任务
     * @param taskName 计划任务中的名称
     */
    @Deprecated
    public static void deleteTask(String taskName) {
        try {
            String cmd = "schtasks /delete /tn \"" + taskName + "\"";

            Runtime.getRuntime().exec(cmd);
            Home.OUTPUT.setText("已移除计划任务: " + taskName);
        } catch (IOException e) {
            Home.OUTPUT.setText("移除计划任务失败: " + taskName);
        }
    }

}
