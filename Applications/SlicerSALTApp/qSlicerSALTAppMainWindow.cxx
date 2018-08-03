/*==============================================================================

  Copyright (c) Kitware, Inc.

  See http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  This file was originally developed by Julien Finet, Kitware, Inc.
  and was partially funded by NIH grant 3P41RR013218-12S1

==============================================================================*/

// Qt includes
#include <QDebug>

// Slicer includes
#include "qSlicerModuleSelectorToolBar.h"
#include "qSlicerModulesMenu.h"
#include "qSlicerModuleManager.h"
#include "qSlicerAbstractModule.h"

// SlicerApp includes
#include "qAppAboutDialog.h"
#include "qSlicerSALTAppMainWindow_p.h"
#include "qSlicerApplication.h"

//-----------------------------------------------------------------------------
// qSlicerSALTAppMainWindowPrivate methods

qSlicerSALTAppMainWindowPrivate::qSlicerSALTAppMainWindowPrivate(qSlicerSALTAppMainWindow& object)
  : Superclass(object)
{
}

//-----------------------------------------------------------------------------
qSlicerSALTAppMainWindowPrivate::~qSlicerSALTAppMainWindowPrivate()
{
}

//-----------------------------------------------------------------------------
void qSlicerSALTAppMainWindowPrivate::init()
{
  Q_Q(qSlicerSALTAppMainWindow);
  this->Superclass::init();
}

//-----------------------------------------------------------------------------
void qSlicerSALTAppMainWindowPrivate::setupUi(QMainWindow * mainWindow)
{
  qSlicerApplication * app = qSlicerApplication::application();

  //----------------------------------------------------------------------------
  // Add actions
  //----------------------------------------------------------------------------
  QAction* helpAboutSlicerAppAction = new QAction(mainWindow);
  helpAboutSlicerAppAction->setObjectName("HelpAboutSlicerSALTAppAction");
  helpAboutSlicerAppAction->setText("About " + app->applicationName());

  //----------------------------------------------------------------------------
  // Calling "setupUi()" after adding the actions above allows the call
  // to "QMetaObject::connectSlotsByName()" done in "setupUi()" to
  // successfully connect each slot with its corresponding action.
  this->Superclass::setupUi(mainWindow);

  //----------------------------------------------------------------------------
  // Configure
  //----------------------------------------------------------------------------
  mainWindow->setWindowIcon(QIcon(":/Icons/Medium/DesktopIcon.png"));

  QPixmap logo(":/LogoFull.png");
#if (QT_VERSION >= QT_VERSION_CHECK(5, 0, 0))
  qreal dpr = sqrt(qApp->desktop()->logicalDpiX()*qreal(qApp->desktop()->logicalDpiY()) / (qApp->desktop()->physicalDpiX()*qApp->desktop()->physicalDpiY()));
  logo.setDevicePixelRatio(dpr);
#endif
  this->LogoLabel->setAlignment(Qt::AlignCenter); // XXX Synx with template ?
  this->LogoLabel->setPixmap(logo);


  // To see any effect of changes over here in the application first delete the .ini file pointed by
  // --settings-path option of the project executable.

  // Hide the toolbars
  this->MainToolBar->setVisible(true);
  this->ModuleSelectorToolBar->setVisible(true);
  //this->ModuleToolBar->setVisible(false);
  //this->ViewToolBar->setVisible(false);
  //this->MouseModeToolBar->setVisible(false);
  //this->CaptureToolBar->setVisible(false);
  //this->ViewersToolBar->setVisible(false);
  this->DialogToolBar->setVisible(false);

  // Hide the menus
  //this->menubar->setVisible(false);
  //this->FileMenu->setVisible(false);
  //this->EditMenu->setVisible(false);
  //this->ViewMenu->setVisible(false);
  //this->LayoutMenu->setVisible(false);
  //this->HelpMenu->setVisible(false);

  // Hide the modules panel
  this->PanelDockWidget->setVisible(false);
  this->DataProbeCollapsibleWidget->setCollapsed(true);
  this->DataProbeCollapsibleWidget->setVisible(false);
  this->StatusBar->setVisible(false);
}

//-----------------------------------------------------------------------------
// qSlicerSALTAppMainWindow methods

//-----------------------------------------------------------------------------
qSlicerSALTAppMainWindow::qSlicerSALTAppMainWindow(QWidget* windowParent)
  : Superclass(new qSlicerSALTAppMainWindowPrivate(*this), windowParent)
{
  Q_D(qSlicerSALTAppMainWindow);
  d->init();
}

//-----------------------------------------------------------------------------
qSlicerSALTAppMainWindow::qSlicerSALTAppMainWindow(
  qSlicerSALTAppMainWindowPrivate* pimpl, QWidget* windowParent)
  : Superclass(pimpl, windowParent)
{
  // init() is called by derived class.
}

//-----------------------------------------------------------------------------
qSlicerSALTAppMainWindow::~qSlicerSALTAppMainWindow()
{
}

//-----------------------------------------------------------------------------
void qSlicerSALTAppMainWindow::on_HelpAboutSlicerSALTAppAction_triggered()
{
  qSlicerAboutDialog about(this);
  about.setLogo(QPixmap(":/Logo.png"));


  QString acknowledgmentText(
      "Supported by: NIH and the Slicer Community.<br /><br />"
      "This work is part of the  National Institute of Health grant titled "
      "<i>Shape Analysis Toolbox for Medical Image Computing Projects</i>.<br /><br />"
      "SlicerSALT is a  software package for medical image segmentation's "
      "shape analysis. <br /><br />"
      "Ongoing development, maintenance, distribution, and training is managed by "
      "Kitware Inc., University of North Carolina, Chapel Hill, M.D. Cancer Center "
      "at The University of Texas and NYU Tandon School of Engineering. <br /><br />");


  about.exec();
}

//-----------------------------------------------------------------------------
void qSlicerSALTAppMainWindow::show()
{
  Q_D(qSlicerSALTAppMainWindow);
  qSlicerModulesMenu* qMenu = d->ModuleSelectorToolBar->modulesMenu();
  qSlicerModuleManager * moduleManager = qSlicerApplication::application()->moduleManager();

  // Modules to add
  QStringList addModuleNames = QStringList()
          << "Home";
  QAction * beforeAction = qMenu->actions().at(1); // to insert after the "All Modules" menu
  foreach(const QString& moduleName, addModuleNames)
    {
    qSlicerAbstractCoreModule * coreModule = moduleManager->module(moduleName);
    qSlicerAbstractModule* module = qobject_cast<qSlicerAbstractModule*>(coreModule);
    qMenu->insertAction(beforeAction, module->action());
    }
  // Add missing separator (only if all modules removed from list)
  beforeAction = qMenu->actions().at(1);
  qMenu->insertSeparator(beforeAction);
  // Show
  this->Superclass::show();
}
