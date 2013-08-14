/*==============================================================================

  Copyright (c) Kitware Inc.

  See COPYRIGHT.txt
  or http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  This file was originally developed by Julien Finet, Kitware Inc.
  and was partially funded by NIH grant 3P41RR013218-12S1

==============================================================================*/

#ifndef __qAppAboutDialog_h
#define __qAppAboutDialog_h

// Qt includes
#include <QDialog>

// CTK includes
#include <ctkPimpl.h>

// SlicerApp includes
#include "qSlicerAppExport.h"

class qAppAboutDialogPrivate;

/// Pre-request that a qApplication has been instanced
class Q_SLICER_APP_EXPORT qAppAboutDialog
  : public QDialog
{
  Q_OBJECT
public:
  qAppAboutDialog(QWidget *parentWidget = 0);
  virtual ~qAppAboutDialog();

protected:
  QScopedPointer<qAppAboutDialogPrivate> d_ptr;

private:
  Q_DECLARE_PRIVATE(qAppAboutDialog);
  Q_DISABLE_COPY(qAppAboutDialog);
};

#endif
