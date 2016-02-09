package saveMyConfigs.config;

import java.util.Set;

/*
[file-bluber-config.xml]
host=bluber
remotepath=/path/config.xml
localpath=bluber1/config.xml
*/
public class Command {
	private String host;
	private String remotePath;
	private String localPath;
	private String how;
	
	/* FIXME: at moment we have following commands:
	 * file    - simple file
	 * dirs    - simple directories
	 * ap451   - wlan access point
	 * pc6428  - dell power connect switch 6248
	 * 
	 * the command are code-wired, that is not good :(
	 */
	
	public Command(String host, String remotePath, String localPath, String how) {
		super();
		this.host = host;
		this.remotePath = remotePath;
		this.localPath = localPath;
		this.how = how;
	}
	
	public static void setCommandConfiguration(ReadINI iniObject)  throws ConfigurationErrorException {
		Set<String> fileKeys = iniObject.getKeys("file-.*");
		Set<String> dirsKeys = iniObject.getKeys("dirs-.*");
		Set<String> ap451Keys = iniObject.getKeys("ap451-.*");
		Set<String> pc6428Keys = iniObject.getKeys("pc6428-.*");
		
		/*
		if(hostsKeys.size()==0) {
			throw new ConfigurationErrorException("errors on read hosts configuration");
		}
		for(String hostconfig : hostsKeys) {
			List<String> hostlist = this.iniObject.getItem(hostconfig);
			
			String hostname=null;
			String ip=null;
			String username=null;
			String password=null;
			for(String s : hostlist) {
				//System.out.println(s);
				String[] s2 = s.split("=");
				if(s2[0].trim().equals("username")) 
					username=s2[1].trim();
				if(s2[0].trim().equals("password")) 
					password=s2[1].trim();
				if(s2[0].trim().equals("host")) 
					hostname=s2[1].trim();
				if(s2[0].trim().equals("ipaddress")) 
					ip=s2[1].trim();
			}
			//System.out.println(hostconfig + " " +hostlist);
			if(username==null || password==null || hostname==null || ip==null) {
				throw new ConfigurationErrorException("errors on read host configuration, element 2lose");
			}
			
			this.hosts.put(hostname, new Host(hostname, ip, username, password));
		}
		if(hosts.size()==0) {
			throw new ConfigurationErrorException("errors on read hosts configuration, no hosts");
		}
		*/
	}
	

	public String getHost() {
		return host;
	}

	public String getRemotePath() {
		return remotePath;
	}

	public String getLocalPath() {
		return localPath;
	}
	
	public String getHow() {
		return how;
	}

}
