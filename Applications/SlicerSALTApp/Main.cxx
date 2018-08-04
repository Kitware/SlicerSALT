/*==============================================================================

  Copyright (c) Kitware, Inc.

  See http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  This file was originally developed by Jean-Christophe Fillion-Robin, Kitware, Inc.
  and was partially funded by NIH grant 3P41RR013218-12S1

==============================================================================*/

// SlicerSALT includes
#include "qSlicerSALTAppMainWindow.h"
#include "Widgets/qAppStyle.h"

// Qt includes
#include <QAction>

// CTK includes
#include <ctkCollapsibleButton.h>

// Slicer includes
#include <qSlicerAbstractCoreModule.h>
#include <qSlicerApplicationHelper.h>
#include <qSlicerLayoutManager.h>
#include <qSlicerModuleManager.h>
#include <qSlicerModulePanel.h>

// MRML includes
#include <vtkMRMLLayoutNode.h>

namespace
{

//----------------------------------------------------------------------------
int SlicerAppMain(int argc, char* argv[])
{
  typedef qSlicerSALTAppMainWindow SlicerMainWindowType;

  qSlicerApplicationHelper::preInitializeApplication(argv[0], new qAppStyle);

  qSlicerApplication app(argc, argv);
  if (app.returnCode() != -1)
    {
    return app.returnCode();
    }

  QScopedPointer<QSplashScreen> splashScreen;
  QScopedPointer<SlicerMainWindowType> window;

  qSlicerApplicationHelper::postInitializeApplication<SlicerMainWindowType>(
        app, splashScreen, window);

  if(!window.isNull())
    {
    QString windowTitle = QString("%1 %2").arg(Slicer_MAIN_PROJECT_APPLICATION_NAME).arg(Slicer_MAIN_PROJECT_VERSION_FULL);
    window->setWindowTitle(windowTitle);

    // Setup Home module
    qSlicerModuleManager * moduleManager = app.moduleManager();
    qSlicerAbstractCoreModule * homeCoreModule = moduleManager->module("Home");
    qSlicerAbstractModule* homeModule = qobject_cast<qSlicerAbstractModule*>(homeCoreModule);
    homeModule->action()->setIcon(window->windowIcon());

    // Open Help & acknowledgment
    qSlicerModulePanel* modulePanel = window->findChild<qSlicerModulePanel*>("ModulePanel");
    ctkCollapsibleButton* helpButton = modulePanel->findChild<ctkCollapsibleButton*>("HelpCollapsibleButton");
    helpButton->setCollapsed(false);

    qSlicerLayoutManager * layoutManager = qSlicerApplication::application()->layoutManager();
    layoutManager->setLayout(vtkMRMLLayoutNode::SlicerLayoutOneUp3DView);
    }

  return app.exec();
}

} // end of anonymous namespace

#include "qSlicerApplicationMainWrapper.cxx"
