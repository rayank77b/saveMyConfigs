package saveMyConfigs.config;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class ENV {
	private String fileNameIni;
	private ReadINI iniObject;
	private GitServerConfig gitServer;
	private SSHServerConfig sshServer;
	private Map<String, HostConnfig> hosts;
	private Map<String, CommandConfig> commands;

	public ENV(String fileNameIni) throws ConfigurationErrorException {
		this.fileNameIni = fileNameIni;
		try {
			this.iniObject = new ReadINI(this.fileNameIni);
		} catch (IOException e) {
			throw new ConfigurationErrorException("errors read INI File");
		}
		this.gitServer = GitServerConfig.setGitServerConfiguration(this.iniObject);
		this.sshServer = SSHServerConfig.setSSHServerConfiguration(this.iniObject);
		this.hosts = new HashMap<String, HostConnfig>();
		HostConnfig.setHostConfiguration(this.iniObject, this.hosts);
		this.commands = new HashMap<String, CommandConfig>();
		CommandConfig.setCommandConfiguration(this.iniObject, this.commands);
		
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

	public HostConnfig getHosts(String hostname) {
		return this.hosts.get(hostname);
	}
	
	public Map<String, CommandConfig> getCommandMap() {
		return this.commands;
	}
	
	public CommandConfig getCommand(String command) {
		return this.commands.get(command);
	}
	
}
