package saveMyConfigs;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import saveMyConfigs.config.ConfigurationErrorException;
import saveMyConfigs.config.ENV;

public class SMC {
	private String configFile;
	private ENV env;
	private Set<String> sCmds;
	private List<Command> cmds;
	
	public SMC(String configFile) {
		this.configFile = configFile;
		this.cmds = new ArrayList<Command>();
		try {
			env = new ENV(configFile);
			
			sCmds = env.getCommandNames();
			System.out.println("following command will be worked: ");
			sCmds.forEach((k)->System.out.println("  " +k));
			
			System.out.println();
			
			for( String sCommand : sCmds) {
				System.out.println("add following command > " + sCommand);
				this.cmds.add(new Command(this.env, sCommand));
			}
		} catch (ConfigurationErrorException e) {
			System.err.println("errors on get the configs from "+configFile);
			System.exit(-1);
		}
	}
	
	public void worksCommands() {
		for( Command cmd : this.cmds) {
			System.out.println("work command: "+cmd.getCommandName());
			//System.out.println(cmd);
			cmd.work();
		}
	}
	
	public String getConfigFile() {
		return this.configFile;
	}
	public int getCommandCount() {
		return this.cmds.size();
	}

	public static void main(String[] args) {
		if(args.length<1) {
			System.err.println("give the configuration file");
			System.exit(-1);
		}
		
		SMC smc = new SMC(args[0]);
		System.out.println("count of commands: " + smc.getCommandCount());
		smc.worksCommands();
		
		
		
	}

}
