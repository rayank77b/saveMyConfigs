package saveMyConfigs;

import java.io.File;
import java.io.IOException;

import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.storage.file.FileRepositoryBuilder;

public class GitRepo {
	private String repoPath;
	Repository existingRepo;
	
	public GitRepo (String repoPath) throws IOException {
		this.repoPath = repoPath;
		
		System.out.println(this.repoPath+"/.git");
		//this.existingRepo = new FileRepositoryBuilder().setGitDir(new File(this.repoPath+"/.git")).build();
		FileRepositoryBuilder repositoryBuilder = new FileRepositoryBuilder();
		System.out.println("new filerepobuilder ok");
		repositoryBuilder.setMustExist( true );
		System.out.println("must ok");
		repositoryBuilder.setGitDir(new File(this.repoPath));
		System.out.println("set git dir ok");
		
		Repository repository = repositoryBuilder.build();
		System.out.println("get repo");
		
	}
}
