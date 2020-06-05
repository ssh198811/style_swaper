import  os
import Ui_test519 as ui
class Get_path():
    def __init__(self):
        # self.ui = ui.Ui_MainWindow()
        self.work_=''
        # self.project_base=self.work_+'/style_transfer/'
        self.style_path=''
        self.dds_path=''
    #dds原图真实路径
    def Real_DDs_path(self):
        return f"{self.work_}/{self.dds_path}"
    #jpg,tga保存地址
    def DdsToJpgPath(self):

        dds_path=self.dds_path.replace("\n","").replace("\\","/")
        work_=self.work_.replace("\n","").replace("\\","/")
        return f"{work_}/style_transfer/{dds_path.replace('.dds','.jpg')}",f"{self.work_}/style_transfer/{dds_path.replace('.dds','.tga')}"
    def GetParentName(self):
        return os.path.dirname(self.dds_path.replace("\n",""))
    def GetStyleName(self):
        return  os.path.basename(self.style_path).split('.')[0]
    #temp预览图保存地址
    def GetTempPath(self):
        style_name=self.GetStyleName()
        parentname=self.GetParentName()
        work_ = self.work_.replace("\n", "").replace("\\", "/")
        return f"{work_}/style_transfer/{parentname}/temp/{style_name}/{os.path.basename(self.dds_path.replace('.dds','.jpg'))}"
    #风格图保存路径
    def GetStylePath(self):
        parentname = self.GetParentName()
        work_ = self.work_.replace("\n", "").replace("\\", "/")
        style_name = self.GetStyleName()
        return f"{work_}/style_transfer/{parentname}/style_output/{style_name}/{os.path.basename(self.dds_path.replace('.dds','.jpg'))}"
    #lerp图
    def GetLerpPath(self):
        parentname = self.GetParentName()
        work_ = self.work_.replace("\n", "").replace("\\", "/")
        style_name = self.GetStyleName()
        return [f"{work_}/style_transfer/{parentname}/lerp_output/{style_name}/{os.path.basename(self.dds_path.replace('.dds', '.jpg'))}",f"{work_}/style_transfer/{parentname}/lerp_output/{style_name}/{os.path.basename(self.dds_path.replace('.dds', '.tga'))}"]
    #dds图
    def GetDdsOutputPath(self):
        parentname = self.GetParentName()
        work_ = self.work_.replace("\n", "").replace("\\", "/")
        style_name = self.GetStyleName()
        return f"{work_}/style_transfer/{parentname}/dds_output/{style_name}/"



    ###############################################################################################################################################################################



    #expanded jpg,tga
    def GetEpandedJpgTgaPath(self):
        parentname = self.GetParentName()
        work_ = self.work_.replace("\n", "").replace("\\", "/")
        # style_name = os.path.basename(self.style_path).split('.')[0]
        return [f"{self.work_}/style_transfer/{parentname}/expanded/{os.path.basename(self.dds_path.replace('.dds', '.jpg'))}",f"{self.work_}/style_transfer/{parentname}/expanded/{os.path.basename(self.dds_path.replace('.dds', '.tga'))}"]
    #expanded-style
    def GetExpandedStylePath(self):
        parentname =self.GetParentName()
        work_ = self.work_.replace("\n", "").replace("\\", "/")
        style_name = self.GetStyleName()
        return f"{self.work_}/style_transfer/{parentname}/expanded/style_output/{style_name}/{os.path.basename(self.dds_path.replace('.dds', '.jpg'))}"
    #expanded_lerp
    def GetExpandedLerpPath(self):
        parentname = self.GetParentName()
        work_ = self.work_.replace("\n", "").replace("\\", "/")
        style_name = self.GetStyleName()
        return [f"{self.work_}/style_transfer/{parentname}/expanded/lerp_output/{style_name}/{os.path.basename(self.dds_path.replace('.dds', '.jpg'))}",f"{work_}/style_transfer/{parentname}/expanded/lerp_output/{style_name}/{os.path.basename(self.dds_path.replace('.dds', '.tga'))}"]
    #seamless
    def GetSeamlessPath(self):
        parentname = self.GetParentName()
        work_ = self.work_.replace("\n", "").replace("\\", "/")
        style_name = self.GetStyleName()
        return f"{self.work_}/style_transfer/{parentname}/expanded/seamless_output/{style_name}/{os.path.basename(self.dds_path.replace('.dds', '.jpg'))}"
    #expanded-dds
    def GetSeamlessDdsPath(self):
        parentname = self.GetParentName()
        work_ = self.work_.replace("\n", "").replace("\\", "/")
        style_name = self.GetStyleName()
        return f"{self.work_}/style_transfer/{parentname}/expanded/dds_output/{style_name}/"


if __name__ == '__main__':
    a=Get_path()
    a.work_='G:\稻香村'
    a.style_path='G:\\test\style_test\莫奈.jpg'
    a.dds_path='data\maps\T_Cliff_062_A.dds'
    print(a.GetExpandedLerpPath())