package saveMyConfigs.config;

import static org.junit.Assert.*;

import java.io.IOException;

import org.junit.Test;

public class TestENV {

	@Test
	public void test() {
		
		ENV env=null;
		try {
			env = new ENV("example12.ini");
			fail("errors, we should not read a non existed ini-file");
		} catch (ConfigurationErrorException e) {
		}
		
		try {
			env = new ENV("example1.ini");
			assertNotNull("env was not created", env);
		} catch (ConfigurationErrorException e) {
			fail("errors on EVN: "+e.errors);
		}
		
		GitServerConfig gsc = env.getGitServer();
		assertEquals("username is false", "name", gsc.getUserName());
		assertEquals("password is false", "pass1", gsc.getPassword());
		assertEquals("repopath is false", "/home/ray/path/toRepo.git", gsc.getRemotePath());
		assertEquals("remote url is false", "http://bla:bla@domain.com:8080/git/TestConfig.git", gsc.getRemoteUrl());
		
		Host host = env.getHosts("bluber");
		assertEquals("username is false", "name", host.getUserName());
	}

}
