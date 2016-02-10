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
		this.gitServerConfig = this.env.getGitServer();
		this.sshServerConfig = this.env.getSSHServer();
		this.commmandConfig = this.env.getCommand(this.commandName);
		this.hostConfig = this.env.getHosts(this.commmandConfig.getHost());
	}
	
	public String getCommandName() {
		return commandName;
	}


	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return "Command [commandName=" + commandName + ", commmandConfig=" + commmandConfig + ", gitServerConfig="
				+ gitServerConfig + ", sshServerConfig=" + sshServerConfig + ", hostConfig=" + hostConfig + ", env="
				+ env + "]";
	}
	
	
	
	

}
