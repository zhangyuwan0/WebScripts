import java.io.File;
import java.io.FileFilter;


public class DeletePDFs {

	public static void main(String[] args) {
		// 父目录
		String targetFolder = "C:\\Users\\Administrator\\Desktop\\文书\\522226\\公诉判决书";
		// 父目录
		File folders = new File(targetFolder);
		// 该文件夹下文件列表
		File[] sonFolders = folders.listFiles();
		for(File sonFolder:sonFolders){
			// 如果是子文件夹
			if(sonFolder.isDirectory()){
				// 删除隐藏文件
				File[] otherFiles = sonFolder.listFiles(new FileFilter() {
					
					@Override
					public boolean accept(File pathname) {
						return pathname.getName().startsWith(".");
					}
				});
				for(File otherFile:otherFiles){
					otherFile.delete();
				}
				// 查找子文件夹下的PDF文件 并删除
				File[] files = sonFolder.listFiles(new FileFilter() {
					
					@Override
					public boolean accept(File pathname) {
						return pathname.getName().endsWith("pdf");
					}
				});
				for(File pdfFile:files){
					pdfFile.delete();
				}
			}
		}
		
	}
}
