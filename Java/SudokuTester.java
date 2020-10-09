package projekt;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertFalse;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class SudokuTester {
	int[][] m;
	SudokuSolver solver;

	@BeforeEach
	public void setUp() throws Exception {
		m = new int[9][9];
		for (int r = 0; r < 9; r++)
			for (int col = 0; col < 9; col++)
				m[r][col] = 0;
		solver = new SudokuSolver();
	}

	@Test
	public final void testSetGetValue() {
		solver.setValue(2, 3, 4);
		assertEquals("Should be zero:", 0, solver.getValue(2, 4));
		assertEquals("Should be 4:", 4, solver.getValue(2, 3));
		solver.setValue(4, 5, 10);
		assertEquals("Values > 9 do not work", 0, solver.getValue(4, 5));
	}

	@Test
	public final void testCheckRow() {
		solver.setValue(2, 3, 4);
		assertTrue("Value should work here:", solver.checkRow(2, 1));
		solver.setValue(2, 4, 1);
		assertFalse("Value 1 already exists, so there will be a 2:", solver.checkRow(2, 1));

	}

	@Test
	public final void testCheckCol() {
		solver.setValue(2, 3, 4);
		assertTrue("Value should work here:", solver.checkCol(3, 1));
		solver.setValue(5, 3, 1);
		assertFalse("Value 1 already exists, so there will be a 2:", solver.checkCol(3, 1));
	}

	@Test
	public final void testCheckSq() {
		solver.setValue(2, 3, 4);
		assertTrue("Value should work in this square:", solver.checkSq(2, 3, 1));
		solver.setValue(2, 4, 1);
		assertFalse("Value 1 already exists, so there will be a 2:", solver.checkSq(2, 3, 1));
	}
	@Test
	public final void ok() {
		solver.setValue(2, 3, 4);
		assertTrue("Value works here", solver.ok(2, 4, 1));
		assertTrue("Value works here", solver.ok(3, 3, 1));
		assertTrue("Value works here", solver.ok(1, 4, 1));
		assertFalse("Value does not work here", solver.ok(2, 4, 4));
		assertFalse("Value does not work here", solver.ok(3, 3, 4));
		assertFalse("Value does not work here", solver.ok(1, 4, 4));
	}

	@Test
	public final void SolveEmpty() {
		assertTrue("Tomt sudoko löst", solver.solve());
	}
	
	@Test
	public final void SolveExample() {
		solver.setValue(0, 2, 8);
		solver.setValue(0, 5, 9);
		solver.setValue(0, 7, 6);
		solver.setValue(0, 8, 2);
		solver.setValue(1, 8, 5);
		solver.setValue(2, 0, 1);
		solver.setValue(2, 2, 2);
		solver.setValue(2, 3, 5);
		solver.setValue(3, 3, 2);
		solver.setValue(3, 4, 1);
		solver.setValue(3, 7, 9);
		solver.setValue(4, 1, 5);
		solver.setValue(4, 6, 6);
		solver.setValue(5, 0, 6);
		solver.setValue(5, 7, 2);
		solver.setValue(5, 8, 8);
		solver.setValue(6, 0, 4);
		solver.setValue(6, 1, 1);
		solver.setValue(6, 3, 6);
		solver.setValue(6, 5, 8);
		solver.setValue(7, 0, 8);
		solver.setValue(7, 1, 6);
		solver.setValue(7, 4, 3);
		solver.setValue(7, 6, 1);
		solver.setValue(8, 6, 4);
		assertTrue("Lösbart", solver.solve());
		assertEquals("Rätt värde:", 3, solver.getValue(1, 0));
		assertEquals("Rätt värde:", 5, solver.getValue(0, 0));
		assertEquals("Rätt värde:", 7, solver.getValue(1, 1));
		assertEquals("Rätt värde:", 6, solver.getValue(2, 4));
		assertEquals("Rätt värde:", 6, solver.getValue(3, 5));
		assertEquals("Rätt värde:", 9, solver.getValue(4, 2));
		assertEquals("Rätt värde:", 9, solver.getValue(5, 3));
		assertEquals("Rätt värde:", 3, solver.getValue(6, 7));
		assertEquals("Rätt värde:", 2, solver.getValue(7, 5));
		assertEquals("Rätt värde:", 6, solver.getValue(8, 8));

	}
	
	@Test
	public final void SolveUnsolvable() {
		solver.setValue(0, 2, 8);
		solver.setValue(0, 5, 9);
		solver.setValue(0, 7, 6);
		solver.setValue(0, 8, 2);
		solver.setValue(1, 8, 5);
		solver.setValue(2, 0, 1);
		solver.setValue(2, 2, 2);
		solver.setValue(2, 3, 5);
		solver.setValue(3, 3, 2);
		solver.setValue(3, 4, 1);
		solver.setValue(3, 7, 9);
		solver.setValue(4, 1, 5);
		solver.setValue(4, 6, 6);
		solver.setValue(5, 0, 6);
		solver.setValue(5, 6, 2);
		solver.setValue(5, 7, 8);
		solver.setValue(6, 0, 4);
		solver.setValue(6, 1, 1);
		solver.setValue(6, 3, 6);
		solver.setValue(6, 5, 8);
		solver.setValue(7, 0, 8);
		solver.setValue(7, 1, 6);
		solver.setValue(7, 4, 3);
		solver.setValue(7, 6, 1);
		solver.setValue(8, 6, 4);
		assertFalse("Ska inte gå att lösa", solver.solve());


	}
}
