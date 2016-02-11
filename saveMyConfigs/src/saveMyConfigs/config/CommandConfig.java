package saveMyConfigs.config;

import java.util.List;
import java.util.Map;
import java.util.Set;

/*
[file-bluber-config.xml]
host=bluber
remotepath=/path/config.xml
localpath=bluber1/config.xml
*/
public class CommandConfig {
	private String command;
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
	
	public CommandConfig(String command, String host, String remotePath, String localPath, String how) {
		this.command = command;
		this.host = host;
		this.remotePath = remotePath;
		this.localPath = localPath;
		this.how = how;
	}
	
	public static CommandConfig getCommand(String name, String command, ReadINI iniObject) throws ConfigurationErrorException  {
		List<String> commandlist = iniObject.getItem(command);
		
		String host=null;
		String remotepath=null;
		String localpath=null;
		String how=null;
		for(String s : commandlist) {
			//System.out.println(s);
			String[] s2 = s.split("=");
			if(s2[0].trim().equals("host")) 
				host=s2[1].trim();
			if(s2[0].trim().equals("remotepath")) 
				remotepath=s2[1].trim();
			if(s2[0].trim().equals("localpath")) 
				localpath=s2[1].trim();
			if(s2[0].trim().equals("how")) 
				how=s2[1].trim();
		}
		if(host==null || remotepath==null || localpath==null || how==null) {
			throw new ConfigurationErrorException("errors on read file command configuration, element 2lose");
		}
		return new CommandConfig(name, host, remotepath, localpath, how);
	}
	
	public static void setCommandConfiguration(ReadINI iniObject, Map<String, CommandConfig> commands)  throws ConfigurationErrorException {
		Set<String> fileKeys = iniObject.getKeys("file-.*");
		Set<String> dirsKeys = iniObject.getKeys("dirs-.*");
		Set<String> ap451Keys = iniObject.getKeys("ap451-.*");
		Set<String> pc6428Keys = iniObject.getKeys("pc6428-.*");
		
		if(fileKeys.size()==0 && 
			dirsKeys.size()==0 &&
			ap451Keys.size()==0 &&
			pc6428Keys.size()==0) {
			throw new ConfigurationErrorException("errors on read hosts configuration, no commands founds");
		}
		
		
		for(String dirs : dirsKeys) {
			CommandConfig c = CommandConfig.getCommand("dirs", dirs, iniObject);
			commands.put(dirs, c);
		}
		for(String file : fileKeys) {
			CommandConfig c = CommandConfig.getCommand("file", file, iniObject);
			commands.put(file, c);
		}
		for(String ap451 : ap451Keys) {
			CommandConfig c = CommandConfig.getCommand("ap451", ap451, iniObject);
			commands.put(ap451, c);
		}
		for(String pc6428 : pc6428Keys) {
			CommandConfig c = CommandConfig.getCommand("pc6428", pc6428, iniObject);
			commands.put(pc6428, c);
		}
	}
	
	public String getCommand() {
		return command;
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

	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return "CommandConfig  [command=" + command + ", host=" + host + ", remotePath=" + remotePath + ", localPath="
				+ localPath + ", how=" + how + "]";
	}
	
	

}
