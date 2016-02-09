package saveMyConfigs.config;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class ENV {
	private String fileNameIni;
	private GitServerConfig gitServer;
	private Map<String, Host> hosts;
	private ReadINI iniObject;
	/**
	 * @param fileNameIni
	 * @throws IOException 
	 */
	public ENV(String fileNameIni) throws ConfigurationErrorException {
		this.fileNameIni = fileNameIni;
		try {
			this.iniObject = new ReadINI(this.fileNameIni);
		} catch (IOException e) {
			throw new ConfigurationErrorException("errors read INI File");
		}
		setGitServerConfiguration();
		hosts = new HashMap<String, Host>();
		setHostConfiguration();
	}
	
	private void setGitServerConfiguration() throws ConfigurationErrorException {
		// FIXME: at moment we use only 1 git-server for save configurations
		List<String> list = iniObject.getItem("git-configs");
		if(list.size()==0) {
			throw new ConfigurationErrorException("errors on read git server configuration");
		}
		String username=null;
		String password=null;
		String repopath=null;
		String remote=null;
		for(String s : list) {
			String[] s2 = s.split("=");
			if(s2[0].trim().equals("username")) 
				username=s2[1].trim();
			if(s2[0].trim().equals("password")) 
				password=s2[1].trim();
			if(s2[0].trim().equals("repopath")) 
				repopath=s2[1].trim();
			if(s2[0].trim().equals("remote")) 
				remote=s2[1].trim();
		}
		if(username==null || password==null || repopath==null || remote==null) {
			throw new ConfigurationErrorException("errors on read git server configuration, element lose");
		}
		this.gitServer=new GitServerConfig(username, password, repopath, remote);
		
	}

	/**
	 * @return the gitServer
	 */
	public GitServerConfig getGitServer() {
		return gitServer;
	}
	
	private void setHostConfiguration()  throws ConfigurationErrorException {
		Set<String> hostsKeys = this.iniObject.getKeys("host-.*");
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
	}
	
	public int getHostsCount() {
		return this.hosts.size();
	}

	/**
	 * @return the hosts
	 */
	public Host getHosts(String hostname) {
		return this.hosts.get(hostname);
	}
	
	
	
	
}
