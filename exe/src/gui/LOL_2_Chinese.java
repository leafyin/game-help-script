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

    public static void main(String[] args) {
        new LOL_2_Chinese();
    }

    public LOL_2_Chinese (){
        SwingUtilities.invokeLater(() -> {
            this.setTitle("英雄联盟外服语言切换工具");
            this.setSize(400, 200);
            this.setDefaultCloseOperation(this.EXIT_ON_CLOSE);

            // 获取屏幕尺寸
            Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
            int x = screenSize.width - this.getWidth();
            int y = screenSize.height - this.getHeight();
            this.setLocation(x, y); // 窗口对齐右下角

            JPanel panel = new JPanel();
            panel.setLayout(new GridBagLayout()); // 使用 GridBagLayout 使下拉框居中

            JComboBox<String> comboBox = getStringJComboBox();
            panel.add(comboBox);

            this.add(panel);
            this.setVisible(true);
        });
    }

    private JComboBox<String> getStringJComboBox() {
        String[] options = {"简体中文", "台服-繁体中文", "欧服", "日服", "韩服", "美国", "新加坡", "马来西亚"};
        JComboBox<String> comboBox = new JComboBox<>(options);
        comboBox.addActionListener(e -> {
            String selectedOption = (String) comboBox.getSelectedItem();
            assert selectedOption != null;
            String lang = switch (selectedOption) {
                case "简体中文" -> "zh_CN";
                case "台服-繁体中文" -> "zh_TW";
                case "欧服" -> "en_GB";
                case "日服" -> "ja_JP";
                case "韩服" -> "ko_KR";
                case "美国" -> "en_US";
                case "新加坡" -> "en_SG";
                case "马来西亚" -> "zh_MY";
                default -> null;
            };
            changeLanguage(lang);
        });
        return comboBox;
    }

    /**
     * 切换语言
     * @param lang: 语言
     */
    public void changeLanguage(String lang) {
        try (BufferedReader reader = new BufferedReader(new FileReader(PATHNAME + FILENAME))) {
            BufferedWriter writer = new BufferedWriter(new FileWriter("D:\\" + FILENAME));
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
            Path source = Path.of("D:\\" + FILENAME);
            Path target = Path.of(PATHNAME + FILENAME);
            Files.move(source, target, StandardCopyOption.REPLACE_EXISTING);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
