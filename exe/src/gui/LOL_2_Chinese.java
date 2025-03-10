package gui;

import javax.swing.*;
import java.awt.*;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

public class LOL_2_Chinese extends JFrame {

    private final static String PATHNAME = "C:\\ProgramData\\Riot Games\\Metadata\\league_of_legends.live\\";
    private final static String FILENAME = "league_of_legends.live.product_settings.yaml";
    private JCheckBox checkBox;
    private JTextField nowLang;

    private final static String[] LANGUAGES = {
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
            "繁体中文（台湾）"
    };

    public static void main(String[] args) {
        new LOL_2_Chinese();
    }

    public LOL_2_Chinese (){
        SwingUtilities.invokeLater(() -> {
            this.setTitle("英雄联盟外服语言切换工具");
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
            JLabel[] comboBoxLabels = {
                    new JLabel("没有D盘请勾选："),
                    new JLabel("选择语言："),
                    new JLabel("当前语言：")
            };
            JComponent[] components = {
                    checkBox = new JCheckBox(),
                    getStringJComboBox(),
                    nowLang = new JTextField()
            };

            nowLang.setEditable(false);
            nowLang.setText(currentLanguage());

            // 布局
            GridBagConstraints gbc = new GridBagConstraints();
            gbc.insets = new Insets(5, 0, 5, 0); // 组件间距
            gbc.fill = GridBagConstraints.HORIZONTAL; // 让组件填充水平空间
            gbc.gridx = 0; // 列索引
            gbc.gridy = 0; // 行索引

            for (int i = 0;i < comboBoxLabels.length;i++) {
                panel.add(comboBoxLabels[i], gbc);
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

    private JComboBox<String> getStringJComboBox() {
        JComboBox<String> comboBox = new JComboBox<>(LANGUAGES);
        comboBox.addActionListener(e -> {
            String selectedOption = (String) comboBox.getSelectedItem();
            assert selectedOption != null;
            String langCode = languageCode(selectedOption);
            changeLanguage(langCode);
        });
        return comboBox;
    }

    public String currentLanguage() {
        String line, languageStr, lang = "";
        try (BufferedReader reader = new BufferedReader(new FileReader(PATHNAME + FILENAME))) {
            while ( (line = reader.readLine()) != null) {
                if (line.split(":")[0].trim().equals("locale")) {
                    languageStr = line.split(":")[1].trim();
                    lang = languageStr.substring(1, languageStr.length() - 1);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return languageName(lang);
    }

    /**
     * 切换语言
     * @param lang: 语言
     */
    public void changeLanguage(String lang) {
        String path = "";
        try (BufferedReader reader = new BufferedReader(new FileReader(PATHNAME + FILENAME))) {
            if (checkBox.isSelected()) {
                System.out.println("No D");
                path = "C:\\ProgramData\\Riot Games\\Metadata\\";
            } else {
                System.out.println("D");
                path = "D:\\";
            }
            BufferedWriter writer = new BufferedWriter(new FileWriter(path + FILENAME));
            String line, languageStr, language;
            while ( (line = reader.readLine()) != null) {
                if (line.split(":")[0].trim().equals("locale")) {
                    languageStr = line.split(":")[1].trim();
                    language = languageStr.substring(1, languageStr.length() - 1);
                    System.out.println("当前语言：" + language);
                    line = line.replace(language, lang);
                    System.out.println("选择语言：" + line);
                }
                writer.write(line);
                writer.newLine();
            }
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        try {
            // 移动文件
            Path source = Path.of(path + FILENAME);
            Path target = Path.of(PATHNAME + FILENAME);
            Files.move(source, target, StandardCopyOption.REPLACE_EXISTING);
        } catch (IOException e) {
            e.printStackTrace();
        }
        nowLang.setText(currentLanguage());
    }

    public String languageName(String languageCode){
        return switch (languageCode) {
            case "ar_AE" -> "阿拉伯语（阿联酋）";
            case "cs_CZ" -> "捷克语";
            case "de_DE" -> "德语";
            case "el_GR" -> "希腊语";
            case "en_AU" -> "英语（澳大利亚）";
            case "en_GB" -> "英语（英国）";
            case "en_PH" -> "英语（菲律宾）";
            case "en_SG" -> "英语（新加坡）";
            case "en_US" -> "英语（美国）";
            case "es_AR" -> "西班牙语（阿根廷）";
            case "es_ES" -> "西班牙语（西班牙）";
            case "es_MX" -> "西班牙语（墨西哥）";
            case "fr_FR" -> "法语";
            case "hu_HU" -> "匈牙利语";
            case "it_IT" -> "意大利语";
            case "ja_JP" -> "日语";
            case "ko_KR" -> "韩语";
            case "pl_PL" -> "波兰语";
            case "pt_BR" -> "葡萄牙语（巴西）";
            case "ro_RO" -> "罗马尼亚语";
            case "ru_RU" -> "俄语";
            case "th_TH" -> "泰语";
            case "tr_TR" -> "土耳其语";
            case "vi_VN" -> "越南语";
            case "zh_MY" -> "简体中文（马来西亚）";
            case "zh_TW" -> "繁体中文（台湾）";
            default -> "未知语言";
        };
    }

    public String languageCode(String languageName) {
        return switch (languageName) {
            case "阿拉伯语（阿联酋）" -> "ar_AE";
            case "捷克语" -> "cs_CZ";
            case "德语" -> "de_DE";
            case "希腊语" -> "el_GR";
            case "英语（澳大利亚）" -> "en_AU";
            case "英语（英国）" -> "en_GB";
            case "英语（菲律宾）" -> "en_PH";
            case "英语（新加坡）" -> "en_SG";
            case "英语（美国）" -> "en_US";
            case "西班牙语（阿根廷）" -> "es_AR";
            case "西班牙语（西班牙）" -> "es_ES";
            case "西班牙语（墨西哥）" -> "es_MX";
            case "法语" -> "fr_FR";
            case "匈牙利语" -> "hu_HU";
            case "意大利语" -> "it_IT";
            case "日语" -> "ja_JP";
            case "韩语" -> "ko_KR";
            case "波兰语" -> "pl_PL";
            case "葡萄牙语（巴西）" -> "pt_BR";
            case "罗马尼亚语" -> "ro_RO";
            case "俄语" -> "ru_RU";
            case "泰语" -> "th_TH";
            case "土耳其语" -> "tr_TR";
            case "越南语" -> "vi_VN";
            case "简体中文（马来西亚）" -> "zh_MY";
            case "繁体中文（台湾）" -> "zh_TW";
            default -> "未知语言";
        };
    }

}
