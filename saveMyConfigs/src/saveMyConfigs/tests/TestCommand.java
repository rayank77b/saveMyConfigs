package saveMyConfigs.tests;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.fail;

import org.junit.Test;

import saveMyConfigs.Command;
import saveMyConfigs.config.ConfigurationErrorException;
import saveMyConfigs.config.ENV;

public class TestCommand {

	@Test
	public void test() {
		ENV env=null;
		try {
			env = new ENV("example1.ini");
			assertNotNull("env was not created", env);
		} catch (ConfigurationErrorException e) {
			fail("errors on EVN: "+e.errors);
		}
		
		Command command1 = new Command(env, "file-bluber-config.xml");
	}

}
