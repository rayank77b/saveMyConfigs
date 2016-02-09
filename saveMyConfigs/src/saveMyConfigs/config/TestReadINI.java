package saveMyConfigs.config;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.junit.Test;

public class TestReadINI {

	@Test
	public void test() {
		ReadINI rini=null;
		try {
			rini = new ReadINI("example1.ini");
		} catch (IOException e) {
			fail("errors on read file");
		}
		assertNotNull("rini was not created", rini);
		
		Map<String, List<String>> m = rini.getLists();
		assertNotNull("hash map was null", m);
		assertEquals("it must be 12 items in example1.ini", 12, m.size());
		List<String> bluber = m.get("dirs-bluber2-hosts");
		String s_bluber=bluber.toString();
		s_bluber=s_bluber.substring(1, s_bluber.length()-1);
		assertTrue("should contains: host=bluber2, remotepath=/etc/blub, localpath=bluber2/blub", 
				s_bluber.toString().compareTo(new String("host=bluber2, remotepath=/etc/blub, localpath=bluber2/blub"))==0);
		
		Set<String> k = rini.getKeys();
		assertNotNull("keys are null", k);
		assertTrue("has no ap541-accessp1 element",  k.contains("ap541-accessp1"));
		
		bluber = rini.getItem("dirs-bluber2-hosts");
		assertNotNull("list is null", bluber);
		assertTrue("bluber must have host=bluber2", "host=bluber2".equals(bluber.get(0)));
		
		k = rini.getKeys("host-.*");
		assertNotNull("keys are null", k);
		assertTrue("has no host-bluber element",  k.contains("host-bluber"));
		//System.out.println(k);
		k = rini.getKeys("host2-.*");
		assertEquals("is not zero size", 0, k.size());
		
		
	}

}
