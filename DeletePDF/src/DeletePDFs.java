import java.io.File;
import java.io.FileFilter;


public class DeletePDFs {

	public static void main(String[] args) {
		// ��Ŀ¼
		String targetFolder = "C:\\Users\\Administrator\\Desktop\\����\\522226\\�����о���";
		// ��Ŀ¼
		File folders = new File(targetFolder);
		// ���ļ������ļ��б�
		File[] sonFolders = folders.listFiles();
		for(File sonFolder:sonFolders){
			// ��������ļ���
			if(sonFolder.isDirectory()){
				// ɾ�������ļ�
				File[] otherFiles = sonFolder.listFiles(new FileFilter() {
					
					@Override
					public boolean accept(File pathname) {
						return pathname.getName().startsWith(".");
					}
				});
				for(File otherFile:otherFiles){
					otherFile.delete();
				}
				// �������ļ����µ�PDF�ļ� ��ɾ��
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
