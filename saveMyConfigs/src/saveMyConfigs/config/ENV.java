package saveMyConfigs.config;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class ENV {
	private String fileNameIni;
	private ReadINI iniObject;
	private GitServerConfig gitServer;
	private SSHServerConfig sshServer;
	private Map<String, Host> hosts;
	private Map<String, Command> commands;
	
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
		this.gitServer = GitServerConfig.setGitServerConfiguration(this.iniObject);
		this.sshServer = SSHServerConfig.setSSHServerConfiguration(this.iniObject);
		this.hosts = new HashMap<String, Host>();
		Host.setHostConfiguration(this.iniObject, this.hosts);
		this.commands = new HashMap<String, Command>();
		Command.setCommandConfiguration(this.iniObject, this.commands);
		
	}
	
	public GitServerConfig getGitServer() {
		return gitServer;
	}
	
	public SSHServerConfig getSSHServer() {
		return sshServer;
	}
		
	public int getHostsCount() {
		return this.hosts.size();
	}

	public Host getHosts(String hostname) {
		return this.hosts.get(hostname);
	}
	
	public Map<String, Command> getCommandMap() {
		return this.commands;
	}
	
}
