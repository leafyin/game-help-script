package gui;

import javax.swing.*;
import java.awt.*;

public class OutputArea extends JTextArea {

    public OutputArea(int rows, int columns) {
        super(rows, columns);
        this.setEditable(false);
        this.setSize(new Dimension(200, 200));
        this.setLineWrap(true);
        this.setWrapStyleWord(true);
    }

    @Override
    public void append(String t) {
        super.append(t + "\r\n");
    }
}
