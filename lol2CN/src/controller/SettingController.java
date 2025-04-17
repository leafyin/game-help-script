package controller;

import gui.Home;

import java.io.IOException;
import java.util.logging.Logger;

public class SettingController {

    private static final Logger logger = Logger.getLogger(SettingController.class.getName());

    public SettingController(){}

    /**
     * 启用开机自启动
     * @param appName 注册表中显示的名称（如"MyApp"）
     * @param appPath 程序的完整路径（如 "C:\MyApp\app.jar"）
     */
    public static void enableAutoStart1(String appName, String appPath) {
        try {
            // 构造注册表命令
            String cmd = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v "
                    + "\"" + appName + "\" /t REG_SZ /d \"" + appPath + "\" /f";

            // 执行命令
            Runtime.getRuntime().exec(cmd);
            Home.OUTPUT.setText("已添加开机自启: " + appName);
        } catch (IOException e) {
            Home.OUTPUT.setText("添加开机自启失败: " + e.getMessage());
        }
    }

    /**
     * 禁用开机自启动
     * @param appName 注册表中的名称
     */
    public static void disableAutoStart1(String appName) {
        try {
            String cmd = "reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v "
                    + "\"" + appName + "\" /f";
            Runtime.getRuntime().exec(cmd);
            Home.OUTPUT.setText("已移除开机自启: " + appName);
        } catch (IOException e) {
            Home.OUTPUT.setText("移除开机自启失败: " + appName);
        }
    }

    /**
     * 启用开机自启动
     * @param taskName 计划任务中显示的名称（如"MyApp"）
     * @param exePath 程序的完整路径（如 "C:\MyApp\app.jar"）
     */
    public static void enableAutoStart(String taskName, String exePath) {
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
     * 禁用开机自启动
     * @param taskName 计划任务中的名称
     */
    public static void disableAutoStart(String taskName) {
        try {
            String cmd = "schtasks /delete /tn \"" + taskName + "\"";

            Runtime.getRuntime().exec(cmd);
            Home.OUTPUT.setText("已移除计划任务: " + taskName);
        } catch (IOException e) {
            Home.OUTPUT.setText("移除计划任务失败: " + taskName);
        }
    }

}
