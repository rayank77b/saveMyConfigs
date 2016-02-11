package saveMyConfigs.tests;

import static org.junit.Assert.fail;

import java.io.IOException;

import org.junit.Test;

import saveMyConfigs.GitRepo;

public class TestGitRepo {

	@Test
	public void test() {
		try {
			GitRepo gr = new GitRepo("/home/afrank/mnt/git/workspace/testAF");
			System.out.println(gr);
		} catch (IOException e) {
			fail("cannot get repo");
		}
	}

}
