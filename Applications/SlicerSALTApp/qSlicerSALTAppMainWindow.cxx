/* Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
   file LICENSE.  */

// Qt includes
#include <QDebug>
#include <QDesktopWidget>
#include <QLabel>

// CTK includes
#include <ctkMenuComboBox.h>

// Slicer includes
#include "qSlicerAboutDialog.h"
#include "qSlicerModuleSelectorToolBar.h"
#include "qSlicerModulesMenu.h"
#include "qSlicerModuleManager.h"
#include "qSlicerAbstractModule.h"

// SlicerApp includes
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
#if (QT_VERSION >= QT_VERSION_CHECK(5, 7, 0))
  QApplication::setAttribute(Qt::AA_UseHighDpiPixmaps);
#endif
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

  QLabel* logoLabel = new QLabel();
  logoLabel->setObjectName("LogoLabel");
  // QIcon stores multiple versions of the image (in different sizes)
  // and uses the most suitable one (depending on DevicePixelRatio).
  // QLabel cannot take a QIcon, therefore we need to get the most suitable
  // QPixmap from the QIcon (base.png, base@2x, ...).
  // To achieve this, we first determine the pixmap size in device independent units,
  // which is the size of the base image (icon.availableSizes().first(), because for that
  // DevicePixelRatio=1.0), and then we retieve the pixmap for this size.
  QIcon icon = QIcon(":/LogoFull.png");
  QPixmap logo = icon.pixmap(icon.availableSizes().first());
  logoLabel->setPixmap(logo);
  this->PanelDockWidget->setTitleBarWidget(logoLabel);


  // To see any effect of changes over here in the application first delete the .ini file pointed by
  // --settings-path option of the project executable.

  // Hide the toolbars
  this->MainToolBar->setVisible(true);
  this->ModuleSelectorToolBar->setVisible(true);
  this->ModuleToolBar->setVisible(false);
  //this->ViewToolBar->setVisible(false);
  //this->MouseModeToolBar->setVisible(false);
  this->CaptureToolBar->setVisible(false);
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

  qSlicerModulesMenu* modulesMenu = this->ModuleSelectorToolBar->modulesMenu();

  

  modulesMenu->setTopLevelCategoryOrder(
        QStringList()
        << "Shape Analysis Toolbox"
        << "Shape Creation"
        << "Shape Analysis"
        << "Groups"
        << "Skeleton, topology"
        << "Surface Models"
        << "Quantification"
        << "Informatics"
        << "Registration"
        << "Utilities"
        );
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

  // XXX: unused, modify slicer to accept setAcknowledgmentText
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
  // Show
  this->Superclass::show();
}
