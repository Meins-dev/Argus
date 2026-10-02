#ifndef AppVersion
#define AppVersion "0.1.0"
#endif

[Setup]
AppId={{5B550920-8FF8-4FE9-AC76-04B019974602}
AppName=Argus
AppVersion={#AppVersion}
DefaultDirName={autopf}\Argus
DefaultGroupName=Argus
OutputDir=..\dist
OutputBaseFilename=ARGUS-{#AppVersion}-windows-x64-setup
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
WizardStyle=modern

[Files]
Source: "..\dist\ARGUS\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\Argus"; Filename: "{app}\ARGUS.exe"
Name: "{autodesktop}\Argus"; Filename: "{app}\ARGUS.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\ARGUS.exe"; Description: "Launch Argus"; Flags: postinstall nowait skipifsilent
