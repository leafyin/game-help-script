package gui;

import controller.LanguageController;
import util.PropertiesConfig;

import javax.swing.*;
import java.awt.*;
import java.util.Hashtable;
import java.util.Properties;
import java.util.logging.Logger;

public class LOL_2_Chinese extends JFrame {

    private static final Logger logger = Logger.getLogger(LOL_2_Chinese.class.getName());
    private final PropertiesConfig propertiesConfig = new PropertiesConfig();
    private final Properties props = PropertiesConfig.getProps();
    private final LanguageController languageController = new LanguageController();
    private JTextField nowLang;
    private JCheckBox isPBE;
    private final String[] LANGUAGES = {
            "简体中文",
            "阿拉伯语（阿联酋）",
            "捷克语",
            "德语",
            "希腊语",
            "英语（澳大利亚）",
            "英语（英国）",
            "英语（菲律宾）",
            "英语（新加坡）",
            "英语（美国）",
            "西班牙语（阿根廷）",
            "西班牙语（西班牙）",
            "西班牙语（墨西哥）",
            "法语",
            "匈牙利语",
            "意大利语",
            "日语",
            "韩语",
            "波兰语",
            "葡萄牙语（巴西）",
            "罗马尼亚语",
            "俄语",
            "泰语",
            "土耳其语",
            "越南语",
            "简体中文（马来西亚）",
            "繁体中文"
    };

    public static void main(String[] args) {
        new LOL_2_Chinese();
    }

    public LOL_2_Chinese (){
        SwingUtilities.invokeLater(() -> {
            this.setTitle("LOL外服语言切换工具");
            int width = 400, height = 200;
            this.setSize(width, height);
            this.setDefaultCloseOperation(this.EXIT_ON_CLOSE);

            // 获取屏幕尺寸，并且居中展示
            Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
            int x = screenSize.width / 2 - width / 2;
            int y = screenSize.height / 2 - height / 2;
            this.setLocation(x, y);

            JPanel panel = new JPanel();
            panel.setLayout(new GridBagLayout());
            JLabel[] labels = {
                    new JLabel("PBE请勾选："),
                    new JLabel("当前客户端语言："),
                    new JLabel("选择语言：")
            };
            JComponent[] components = {
                    isPBE = new JCheckBox(),
                    nowLang = new JTextField(),
                    this.getStringJComboBox()
            };

            isPBE.addActionListener(e -> {
                if (isPBE.isSelected()) {
                    props.setProperty("isPBE", "true");
                } else {
                    props.setProperty("isPBE", "false");
                }
                PropertiesConfig.save(props);
            });

            // 配置
            Hashtable<String, Object> config = propertiesConfig.getConfig();
            isPBE.setSelected((Boolean) config.get("isPBE"));
            languageController.changeLanguage(isPBE, nowLang, (String) config.get("lang"));
            nowLang.setText(languageController.currentLanguage());
            nowLang.setEditable(false);

            // Timer
            languageController.changeTimer((String) config.get("lang"), isPBE);

            // 布局
            GridBagConstraints gbc = new GridBagConstraints();
            gbc.insets = new Insets(5, 0, 5, 0); // 组件间距
            gbc.fill = GridBagConstraints.HORIZONTAL; // 让组件填充水平空间
            gbc.gridx = 0; // 列索引
            gbc.gridy = 0; // 行索引

            for (int i = 0;i < labels.length;i++) {
                panel.add(labels[i], gbc);
                gbc.gridx++;
                panel.add(components[i], gbc);
                if (gbc.gridx == 1) {
                    gbc.gridx = 0;
                }
                gbc.gridy++;
            }

            this.add(panel);
            this.setVisible(true);
        });
    }

    /**
     * 语言选择下拉框
     * @return comboBox
     */
    private JComboBox<String> getStringJComboBox() {
        JComboBox<String> comboBox = new JComboBox<>(LANGUAGES);
        comboBox.addActionListener(e -> {
            String selectedOption = (String) comboBox.getSelectedItem();
            assert selectedOption != null;
            String langCode = languageController.languageCode(selectedOption);
            languageController.changeLanguage(isPBE, nowLang, langCode);
            props.setProperty("lang", langCode);
            PropertiesConfig.save(props);
        });
        return comboBox;
    }

}
