package saveMyConfigs.config;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.fail;

import java.util.Map;

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
		
		SSHServerConfig sshsc = env.getSSHServer();
		assertEquals("username is false", "bla", sshsc.getUserName());
		assertEquals("password is false", "111111", sshsc.getPassword());
		
		HostConnfig host = env.getHosts("bluber");
		assertEquals("username is false", "name", host.getUserName());
		assertEquals("we have 4 host in example ini", 4, env.getHostsCount());
		
		Map<String, CommandConfig> c = env.getCommandMap();
		//c.forEach((k,v)->System.out.println(k));
		assertEquals("should be 5 commands in example ini", 5, c.size());
		CommandConfig fileCommand1 = env.getCommand("file-bluber-config.xml");
		assertEquals("should be file", "file", fileCommand1.getCommand());
		assertEquals("should be remotepath /path/config.xml", "/path/config.xml", fileCommand1.getRemotePath());
		
	}

}
