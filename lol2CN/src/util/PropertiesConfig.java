package util;

import gui.Home;

import javax.swing.*;
import java.io.*;
import java.util.Hashtable;
import java.util.Properties;

public class PropertiesConfig {

    private Hashtable<String, Object> config;

    public Hashtable<String, Object> getConfig() {
        return config;
    }

    public void setConfig(Properties props) {
        Hashtable<String, Object> config = new Hashtable<>();
        config.put("startup", Boolean.parseBoolean(props.getProperty("startup")));
        config.put("isPBE", Boolean.parseBoolean(props.getProperty("isPBE")));
        config.put("lang", props.getProperty("lang"));
        this.config = config;
    }
    private static final String CONFIG_DIR = ".\\conf\\";
    private static final String CONFIG_NAME = "config.properties";

    public PropertiesConfig() {
        try {
            Properties props = new Properties();
            File file = new File(CONFIG_DIR);
            if (!file.exists()) {
                if (file.mkdir()) {
                    file = new File(CONFIG_DIR + CONFIG_NAME);
                    if (file.createNewFile()) {
                        props.setProperty("startup", "false");
                        props.setProperty("isPBE", "false");
                        props.setProperty("lang", "zh_CN");
                        save(props);
                        Home.OUTPUT.append("配置文件已创建");
                    } else {
                        Home.OUTPUT.append("配置文件创建失败");
                    }
                } else {
                    Home.OUTPUT.append("文件加创建失败");
                }
                this.setConfig(getProps());
            } else {
                this.setConfig(getProps());
            }
        } catch (IOException e) {
            JOptionPane.showMessageDialog(
                    null,
                    e.getMessage(),
                    "错误",
                    JOptionPane.ERROR_MESSAGE
            );
        }
    }

    public static Properties getProps(Properties props) {
        try {
            props.load(new FileInputStream(CONFIG_DIR + CONFIG_NAME));
        } catch (IOException e) {
            JOptionPane.showMessageDialog(
                    null,
                    e.getMessage(),
                    "错误",
                    JOptionPane.ERROR_MESSAGE
            );
        }
        return props;
    }

    public static Properties getProps() {
        Properties props = new Properties();
        try {
            props.load(new FileInputStream(CONFIG_DIR + CONFIG_NAME));
        } catch (IOException e) {
            JOptionPane.showMessageDialog(
                    null,
                    e.getMessage(),
                    "错误",
                    JOptionPane.ERROR_MESSAGE
            );
        }
        return props;
    }

    public static void save(Properties props) {
        try (OutputStream output = new FileOutputStream(CONFIG_DIR + CONFIG_NAME)) {
            props.store(output, "Updated configuration");
            Home.OUTPUT.append("配置已保存");
        } catch (IOException e) {
            JOptionPane.showMessageDialog(
                    null,
                    "无法保存配置文件: " + e.getMessage(),
                    "错误",
                    JOptionPane.ERROR_MESSAGE
            );
        }
    }

}
