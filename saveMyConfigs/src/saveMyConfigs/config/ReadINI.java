package saveMyConfigs.config;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class ReadINI {
	private String name;
	private Map<String, List<String>> lists;
		
	public ReadINI(String filename) throws IOException {
		this.name = filename;
		lists = new HashMap<String, List<String>>();
		
		BufferedReader br = new BufferedReader(new FileReader(filename));
		String line;
		String title=null;
		List <String> l = null;
		
		while ((line = br.readLine()) != null) {
			if ( line.matches("^#.*")) {
				//System.out.println(line); get comment out
		    	continue;
		    }
		    if ( line.matches("\\[.*\\]")) {
		    	//System.out.println(line);
		    	if(title!=null) {
		    		if(l!=null)
		    			lists.put(title, l);
		    		l=null;
		    	}
		    	title=line.substring(1, line.length()-1);
		    }
		    if ( line.contains("=")) {
		    	//System.out.println(line);
		    	if(l==null) {
		    		l=new  ArrayList<String>();
		    		l.add(line);
		    	} else {
		    		l.add(line);
		    	}
		    }
		}
		if(title!=null)
			if(l!=null)
				lists.put(title, l);
		br.close();
	}
	
	public List<String> getItem(String item) {
		return lists.get(item);
	}
	
	public Set<String> getKeys() {
		return lists.keySet();
	}
	
	public Map<String, List<String>> getLists() {
		return lists;
	}

	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return "ReadINI [lists=" + lists + "]";
	}
	
	
	

}
