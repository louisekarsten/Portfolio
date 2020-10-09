package projekt;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridLayout;
import java.util.ArrayList;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

public class SudokuGraphic {
	SudokuSolver solver;

	public static final Color VERY_LIGHT_BLUE = new Color(51, 204, 255);
	private ArrayList<JTextField> fieldList = new ArrayList<JTextField>();
	private ArrayList<Integer> rowList = new ArrayList<Integer>();
	private ArrayList<Integer> colList = new ArrayList<Integer>();

	public SudokuGraphic(SudokuSolver solver) {
		this.solver = solver;
		SwingUtilities.invokeLater(() -> createWindow(solver, "SUDOKU SOLVER", 100, 300));
	}

	public void createWindow(SudokuSolver solver, String title, int width, int height) {
		int r = 0;
		int c = 0;

		JFrame frame = new JFrame(title);
		frame.setMinimumSize(new Dimension(500, 600));
		frame.setMaximumSize(new Dimension(500, 600));
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		Container pane = frame.getContentPane();
		frame.pack();
		frame.setVisible(true);

		JButton solve = new JButton("SOLVE");
		JButton clear = new JButton("CLEAR");
		JPanel panel1 = new JPanel();
		Font font = new Font("Courir", Font.PLAIN, 30);
		GridLayout grid = new GridLayout(9, 9);

		for (int i = 0; i < 81; i++) {
			JTextField ruta = new JTextField();
			ruta.setFont(font);
			ruta.setHorizontalAlignment(JTextField.CENTER);
			if (c == 9) {
				c = 0;
				r++;
			}
			if ((c < 3 || c > 5 && c < 9) && (r < 3 || r > 5)) {
				ruta.setBackground(VERY_LIGHT_BLUE);
			}
			if ((r > 2 && r < 6) && (c > 2 && c < 6)) {
				ruta.setBackground(VERY_LIGHT_BLUE);
			}
			panel1.add(ruta);
			fieldList.add(ruta);
			rowList.add(r);
			colList.add(c);
			c++;
		}
		panel1.setLayout(grid);

		JPanel panel2 = new JPanel();
		panel2.add(solve);
		panel2.add(clear);
		pane.add(panel2);
		pane.setLayout(new BorderLayout());
		pane.add(panel1);
		pane.add(panel2, BorderLayout.SOUTH);

		solve.addActionListener(ActionPerformed -> {

			int value = 0;
			for (int i = 0; i < 81; i++) {
				int row = rowList.get(i);
				int col = colList.get(i);
				JTextField ruta = fieldList.get(i);
				String text = ruta.getText();
				if (text.equals("")) {
					value = 0;
					solver.setValue(row, col, value);
				} else {
					for (char tecken : text.toCharArray()) {
						if (Character.isDigit(tecken) == false || tecken == 0 && tecken != ' '
								|| Integer.parseInt(text) > 9 || Integer.parseInt(text) < 1) {
							JOptionPane.showMessageDialog(frame,
									"Endast siffror 1-9 tillåtna. Tryck på Ok för att försöka igen.", "Error",
									JOptionPane.PLAIN_MESSAGE, null);
							clearSolver();
							return;
						} else {
							value = Integer.parseInt(text);
							if (solver.ok(row, col, value) == false) {
								JOptionPane.showMessageDialog(frame,
										"Olösbart: Ingen av siffrorna får förekomma \n mer än en gång per rad, kolumn eller region. \n Tryck på Ok för att försöka igen.",
										"Error", JOptionPane.PLAIN_MESSAGE, null);
								clearSolver();
								return;
							} else {
								solver.setValue(row, col, value);
							}
						}
					}
				}
			}
			if (solver.solve()) {
				for (int i = 0; i < 81; i++) {
					value = solver.getValue(rowList.get(i), colList.get(i));
					fieldList.get(i).setText(Integer.toString(value));
				}
				for (int j = 0; j < 81; j++) {
					solver.setValue(rowList.get(j), colList.get(j), 0);
				}
			} else {
				JOptionPane.showMessageDialog(frame, "Olösbart. Tryck på Ok för att försöka igen.", "Error",
						JOptionPane.PLAIN_MESSAGE, null);
				clearSolver();
			}
		});

		clear.addActionListener(ActionPerformed -> {
			clear();
		});
	}

	public void clear() {
		for (JTextField field : fieldList) {
			field.setText("");
		}
		clearSolver();
	}
	
	public void clearSolver() {
		for (int j = 0; j < 81; j++) {
			solver.setValue(rowList.get(j), colList.get(j), 0);
		}
	}
}
