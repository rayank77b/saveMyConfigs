package saveMyConfigs;

import saveMyConfigs.config.CommandConfig;
import saveMyConfigs.config.ENV;
import saveMyConfigs.config.GitServerConfig;
import saveMyConfigs.config.HostConnfig;
import saveMyConfigs.config.SSHServerConfig;

public class Command {
	private String commandName;
	private CommandConfig commmandConfig;
	private GitServerConfig gitServerConfig;
	private SSHServerConfig sshServerConfig;
	private HostConnfig hostConfig;
	
	private ENV env;

	public Command(ENV env, String commandName) {
		this.env = env;
		this.commandName = commandName;
		
	}
	
	
	

}
